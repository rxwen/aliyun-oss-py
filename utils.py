# coding: utf-8

from __future__ import print_function, unicode_literals

import bottle
import os
from threading import Thread, Event
import webbrowser
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler, make_server

from boxsdk import OAuth2


CLIENT_ID = 'b0cvaoksdargnpoya4gkwkpuk0arocvg'  # Insert Box client ID here
CLIENT_SECRET = 'SOO2tMVAMbmkSsWMcrOEjZ5fhIo3hYGs'  # Insert Box client secret here
ACCESS_TOKEN = None
OSS_BUCKET = None
OSS_ENDPOINT = None


def authenticate(oauth_class=OAuth2):
    class StoppableWSGIServer(bottle.ServerAdapter):

        def __init__(self, *args, **kwargs):
            super(StoppableWSGIServer, self).__init__(*args, **kwargs)
            self._server = None

        def run(self, app):
            server_cls = self.options.get('server_class', WSGIServer)
            handler_cls = self.options.get('handler_class', WSGIRequestHandler)
            self._server = make_server(
                self.host, self.port, app, server_cls, handler_cls)
            self._server.serve_forever()

        def stop(self):
            self._server.shutdown()

    auth_code = {}
    auth_code_is_available = Event()

    local_oauth_redirect = bottle.Bottle()

    @local_oauth_redirect.get('/')
    def get_token():
        auth_code['auth_code'] = bottle.request.query.code
        auth_code['state'] = bottle.request.query.state
        auth_code_is_available.set()

    local_server = StoppableWSGIServer(host='localhost', port=8080)
    server_thread = Thread(
        target=lambda: local_oauth_redirect.run(server=local_server))
    server_thread.start()

    oauth = oauth_class(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
    auth_url, csrf_token = oauth.get_authorization_url('http://localhost:8080')
    import auto_grant
    # auto_grant.grant_access(auth_url)
    webbrowser.open(auth_url)

    auth_code_is_available.wait()
    local_server.stop()
    assert auth_code['state'] == csrf_token
    access_token, refresh_token = oauth.authenticate(auth_code['auth_code'])

    print('access_token: ' + access_token)
    print('refresh_token: ' + refresh_token)

    global ACCESS_TOKEN
    ACCESS_TOKEN = access_token

    return oauth, access_token, refresh_token


def auth_client():
    oauth = OAuth2(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        access_token=ACCESS_TOKEN
    )
    from boxsdk import Client

    client = Client(oauth)

    me = client.user(user_id='me').get()
    print('user_login: ', me['login'])
    return client

import oss2


def oss_get_bucket():
    auth = oss2.Auth(CLIENT_ID, CLIENT_SECRET)
    bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET)
    return bucket


def oss_put_file(bucket, src, dest, overwrite=True):
    dest_on_oss = oss_convert_filename(dest, False)
    if not overwrite:
        if bucket.object_exists(dest_on_oss):
            raise Exception("%s already exists in bucket %s!" %
                            (dest_on_oss, OSS_BUCKET))
    bucket.put_object_from_file(dest_on_oss, src)


def oss_convert_filename(filename, from_oss=True):
    if from_oss:
        if filename[0] == '?':
            output = '/' + filename[1:]
        elif filename[0] == ';':
            output = '\\' + filename[1:]
    else:
        if filename[0] == '/':
            output = '?' + filename[1:]
        elif filename[0] == '\\':
            output = ';' + filename[1:]
    return output

if __name__ == '__main__':
    authenticate()
#    auth_client()
    os._exit(0)

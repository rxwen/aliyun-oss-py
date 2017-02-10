#!/usr/bin/python
# -*- coding: utf-8 -*-

import warnings
warnings.filterwarnings("ignore")

import os
import sys
import getopt
import utils


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "f:d", ["overwrite"])
        if len(args) != 2:
            raise Exception()
            pass
        if args[1] == '.':
            args[1] = os.path.abspath(args[0])
    except:
        print "Usage:"
        print "upload:   ", sys.argv[0], "[-f config.yaml] [--overwrite] SRC_FILE FOO/BAR/DEST_FILE"
        print "download: ", sys.argv[0], "[-f config.yaml] [-d] SRC_FILE_ON_ALIYUN LOCAL/FOO/BAR/DEST_FILE"
        print "   -f default to ~/.ossclient.yml if not specified"
        return

    argDict = dict(opts)
    overwrite = '--overwrite' in argDict
    config_file = argDict.get('-f', os.path.expanduser("~/.ossclient.yml"))
    download = argDict.get('-d') is not None

    # config = yaml.load(file(config_file))
    config = utils.load_config(config_file)

    utils.CLIENT_ID = config.get('client_id', utils.CLIENT_ID)
    utils.CLIENT_SECRET = config.get('client_secret', utils.CLIENT_SECRET)
    utils.OSS_BUCKET = config.get('oss_bucket', utils.OSS_BUCKET)
    utils.OSS_ENDPOINT = config.get('oss_endpoint', utils.OSS_ENDPOINT)

    try:
        bucket = utils.oss_get_bucket()
        if download:
            marker = None
            while True:
                print "reading info of ", args[0]
                list_result = bucket.list_objects(args[0], marker=marker)
                marker = list_result.next_marker
                src_files = [i.key for i in list_result.object_list]
                for src_file in src_files:
                    dest_file = os.path.join(args[1], src_file)
                    dest_path = os.path.dirname(dest_file)
                    if not os.path.exists(dest_path):
                        os.makedirs(dest_path)

                    # check if this src_file is a file
                    if src_file[-1] not in ["/", "\\"]:
                        if not overwrite:
                            if os.path.exists(dest_file):
                                raise Exception(
                                    "local file already exists: %s" % dest_file)
                        print "downloading:", dest_file
                        bucket.get_object_to_file(src_file, dest_file)
                if not list_result.is_truncated:
                    break
        else:
            if os.path.isdir(args[0]):
                for pair in utils.list_files(args[0], args[1]):
                    print "uploading:", pair[0], " to ", "http://%s.%s/%s"%(utils.OSS_BUCKET,utils.OSS_ENDPOINT,pair[1])
                    utils.uploadoss_put_file(bucket, pair[0], pair[1], overwrite)
                # raise Exception("This is a folder!")
                pass
            else:
                print "uploading:", args[0], " to ", "http://%s.%s/%s"%(utils.OSS_BUCKET,utils.OSS_ENDPOINT,args[1])
                utils.oss_put_file(bucket, args[0], args[1], overwrite)
        print("Success!")
    except Exception, e:
        print e
        print("Failed!")
    return


if __name__ == '__main__':
    main(sys.argv[1:])

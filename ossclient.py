#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import getopt
import utils


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "f:", ["overwrite"])
        if len(args) != 2:
            raise Exception()
            pass
        if args[1] == '.':
            args[1] = os.path.abspath(args[0])
    except:
        print "Usage:"
        print sys.argv[0], "[-f config.yaml] [--overwrite] SRC_FILE FOO/BAR/DEST_FILE"
        return

    argDict = dict(opts)
    overwrite = '--overwrite' in argDict
    config_file = argDict.get('-f', "config.yaml")

    # config = yaml.load(file(config_file))
    config = utils.load_config(config_file)

    utils.CLIENT_ID = config.get('client_id', utils.CLIENT_ID)
    utils.CLIENT_SECRET = config.get('client_secret', utils.CLIENT_SECRET)
    utils.OSS_BUCKET = config.get('oss_bucket', utils.OSS_BUCKET)
    utils.OSS_ENDPOINT = config.get('oss_endpoint', utils.OSS_ENDPOINT)

    try:
        bucket = utils.oss_get_bucket()
        utils.oss_put_file(bucket, args[0], args[1], overwrite)
        print("Success!")
    except Exception, e:
        print e
        print("Failed!")
    return


if __name__ == '__main__':
    main(sys.argv[1:])


import oss2

CLIENT_ID = 'b0cvaoksdargnpoya4gkwkpuk0arocvg'
CLIENT_SECRET = 'SOO2tMVAMbmkSsWMcrOEjZ5fhIo3hYGs'
OSS_BUCKET = None
OSS_ENDPOINT = None


def load_config(filename):
    config = {}
    file = None
    try:
        file = open(filename, 'r')
        for line in file.readlines():
            pair = line.split(':')
            if len(pair) < 2:
                continue
            config[pair[0].strip()] = pair[1].strip()
    except Exception as err:
        print "error loading filename ", err
    finally:
        if file:
            file.close()

    return config


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
    output = filename
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


def list_files(src_folder, dest_folder):
    import os
    ret = []
    for item in os.listdir(src_folder):
        node = os.path.join(src_folder, item)
        dest_node = os.path.join(dest_folder, item)
        if os.path.isfile(node):
            ret.append((node, dest_node))
        elif os.path.isdir(node):
            sub_ret = list_files(node, dest_node)
            ret.extend(sub_ret)
    return ret


if __name__ == '__main__':
    pass

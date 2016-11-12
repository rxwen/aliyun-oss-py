
import oss2

CLIENT_ID = 'b0cvaoksdargnpoya4gkwkpuk0arocvg'
CLIENT_SECRET = 'SOO2tMVAMbmkSsWMcrOEjZ5fhIo3hYGs'
OSS_BUCKET = None
OSS_ENDPOINT = None


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
    pass

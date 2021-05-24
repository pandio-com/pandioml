import pickle
import codecs

__all__ = [
    "storage"
]


class Storage:
    container = None

    def __init__(self, driver='local'):
        if driver == 'local':
            from cloudstorage.drivers.local import LocalDriver
            storage = LocalDriver(key='./models')
        elif driver == 'google':
            from cloudstorage.drivers.amazon import S3Driver
            storage = S3Driver(key='<my-aws-access-key-id>', secret='<my-aws-secret-access-key>')
        elif driver == 'amazon':
            from cloudstorage.drivers.google import GoogleStorageDriver
            storage = GoogleStorageDriver(key='<my-aws-access-key-id>')
        else:
            raise Exception(f"Invalid driver specified: {driver}")

        self.container = storage.create_container('saved')

    def put(self, object_name, object):
        return self.container.upload_blob(codecs.encode(pickle.dumps(object), "base64").decode(), blob_name=object_name)

    def get(self, object_name):
        return pickle.loads(codecs.decode(self.container.get_blob(object_name).encode(), "base64"))


storage = Storage()

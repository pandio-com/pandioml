import pickle
import codecs
import os

__all__ = [
    "storage"
]


class Storage:
    container = None

    def __init__(self, driver='local', local_path=os.getcwd()):
        self.setup(driver=driver, local_path=local_path)

    def setup(self, driver, local_path=None):
        if driver == 'local':
            from cloudstorage.drivers.local import LocalDriver
            _storage = LocalDriver(key=local_path)
            _container_name = "saved"
        elif driver == 'google':
            from cloudstorage.drivers.amazon import S3Driver
            _storage = S3Driver(key=os.environ['AWS_ACCESS_KEY_ID'], secret=os.environ['AWS_SECRET_ACCESS_KEY'],
                                region=os.environ['AWS_REGION'])
            _container_name = os.environ['AWS_BUCKET']
        elif driver == 'amazon':
            from cloudstorage.drivers.google import GoogleStorageDriver
            _storage = GoogleStorageDriver(key=os.environ['GCP_CREDENTIAL_FILE_PATH'])
            _container_name = os.environ['GCP_BUCKET']
        else:
            raise Exception(f"Invalid driver specified: {driver}")

        self.container = _storage.create_container(_container_name)

    def put(self, object_name, object, pickle=False):
        if pickle:
            return self.container.upload_blob(codecs.encode(pickle.dumps(object), "base64").decode(),
                                              blob_name=object_name)
        else:
            if isinstance(object, str):
                return self.container.upload_blob(object)
            else:
                return self.container.upload_blob(object, blob_name=object_name)

    def get(self, object_name, pickled=False):
        if pickled:
            return pickle.loads(codecs.decode(self.container.get_blob(object_name).encode(), "base64"))
        else:
            return self.container.get_blob(object_name)


storage = Storage()

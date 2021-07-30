import pickle
import time
from pandioml.core.storage import storage


class ArtifactStorage:
    def save(self, checkpoint=False):
        if self.get_pipeline_id() is None:
            print("Cannot save artifacts, no pipeline id found.")
            return False

        storage_location = self.get_pipeline_id() + '/' + self.get_name_id()

        if checkpoint:
            storage_location += "/checkpoint"
        else:
            storage_location += "/completed"

        storage_location = storage_location + "/" + time.strftime("%Y%m%d-%H%M%S")

        print(f"Saving artifacts to {storage_location}")

        for item in self._artifacts.items():
            if callable(item[1]):
                print(f"Calling method for {item[0]}")
                try:
                    tmp_file = item[1]()
                    storage.put(f"{storage_location}/pipeline_files.zip", f"{storage_location}/pipeline_files.zip")
                except Exception as e:
                    print(f"An error occurred saving artifact {item[0]}: {e}")
            else:
                print(f"Saving artifact with name: {item[0]}")
                try:
                    storage.put(f"{storage_location}/{item[0]}.pickle", item[1])
                except Exception as e:
                    print(f"An error occurred saving artifact {item[0]}: {e}")

        return True

    def load(self, object_name):
        if self.get_pipeline_id() is None:
            print("Cannot load artifact, no pipeline id found.")
            return False

        return storage.get(object_name)


class FileStorage:
    def save(self, checkpoint=False):
        if self.get_pipeline_id() is None:
            print("Cannot save artifacts, no pipeline id found.")
            return False

        import os.path

        storage_location = self._storage_location + '/' + self.get_pipeline_id() + '/' + self.get_name_id()

        if checkpoint:
            storage_location += "/checkpoint"
        else:
            storage_location += "/completed"

        storage_location = storage_location + "/" + time.strftime("%Y%m%d-%H%M%S")

        print(f"Saving artifacts to {storage_location}")

        os.makedirs(storage_location)

        for item in self._artifacts.items():
            if callable(item[1]):
                print(f"Calling method for {item[0]}")
                try:
                    item[1](storage_location)
                except Exception as e:
                    print(f"An error occurred saving artifact {item[0]}: {e}")
            else:
                print(f"Saving artifact with name: {item[0]}")
                try:
                    # Don't overwrite existing file, this shouldn't happen, but make sure it does not.
                    if not os.path.isfile(f"{storage_location}/{item[0]}.pickle"):
                        with open(f"{storage_location}/{item[0]}.pickle", 'wb') as handle:
                            pickle.dump(item[1], handle)
                except Exception as e:
                    print(f"An error occurred saving artifact {item[0]}: {e}")

        return True


class Artifact(ArtifactStorage):
    _artifacts = {}
    _pipeline_id = None
    _name_id = 'example'
    _config = None

    def __init__(self):
        super().__init__()

    def add(self, _unique_name, _artifact):
        self._artifacts[_unique_name] = _artifact
        return _artifact

    @staticmethod
    def set_storage_location(storage_location):
        storage.setup('local', local_path=storage_location)

    def set_pipeline_id(self, pipeline_id):
        self._pipeline_id = pipeline_id

    def set_name_id(self, name_id):
        self._name_id = name_id

    def get_pipeline_id(self):
        return self._pipeline_id

    def get_name_id(self):
        return self._name_id


artifact = Artifact()

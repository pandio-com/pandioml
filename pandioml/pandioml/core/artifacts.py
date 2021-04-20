from abc import abstractmethod
import pickle


class FileStorage:
    def save(self, directory_wo_slash='/tmp'):
        import os.path
        try:
            os.makedirs(directory_wo_slash)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        for _name, _artifact in self._artifacts:
            # Don't overwrite existing file, this shouldn't happen, but make sure it does not.
            if not os.path.isfile(f"{directory_wo_slash}/{_name}.pickle"):
                with open(f"{directory_wo_slash}/{_name}.pickle", 'wb') as handle:
                    pickle.dump(_artifact, handle)

        return True


class S3Storage:
    def __init__(self):
        self.client = None

    def save(self):
        print(f"Using client to save ({len(self._artifacts)}) element(s).")
        return True


class Artifact(FileStorage):
    _artifacts = []

    def __init__(self):
        super().__init__()

    def add(self, _unique_name, _artifact):
        self._artifacts.append((_unique_name, _artifact))
        return _artifact


artifact = Artifact()

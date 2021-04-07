import pickle
import codecs


class ModelUtility:
    @staticmethod
    def upload(model_name, model, storage):
        if model_name is not None:
            return storage.set(model_name, codecs.encode(pickle.dumps(model), "base64").decode())
            #return storage.set(model_name, pickle.dumps(model, 0).decode())
        else:
            return False

    @staticmethod
    def download(model_name, storage):
        if model_name is not None:
            state = storage.get(model_name)
            if state is not None:
                return pickle.loads(codecs.decode(state.encode(), "base64"))
                #return pickle.loads(state)

        return None

    @staticmethod
    def combine(model_a, model_b):
        #model_a.estimators_ += model_b.estimators_
        #model_a.n_estimators = len(model_a.estimators_)
        #return model_a
        return model_a

import os
import pickle


class ModelUtility:
    @staticmethod
    def upload(model):
        return pickle.dump(model, open(str(os.getcwd()) + '/example.model', 'wb'))

    @staticmethod
    def download(model_name):
        if os.path.exists(str(os.getcwd()) + '/' + model_name):
            return pickle.load(open(str(os.getcwd()) + '/' + model_name, 'rb'))
        else:
            return None

    @staticmethod
    def combine(model_a, model_b):
        model_a.estimators_ += model_b.estimators_
        model_a.n_estimators = len(model_a.estimators_)
        return model_a

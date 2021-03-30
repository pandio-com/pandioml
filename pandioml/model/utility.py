import os
import pickle


class ModelUtility:
    @staticmethod
    def upload(model_name, model, context):
        return context.put_state(model_name, pickle.dumps(model, 0))

    @staticmethod
    def download(model_name, context):
        state = context.get_state(model_name)
        if state is not None:
            return pickle.loads(state)

        return None

    @staticmethod
    def combine(model_a, model_b):
        #model_a.estimators_ += model_b.estimators_
        #model_a.n_estimators = len(model_a.estimators_)
        #return model_a
        return model_a

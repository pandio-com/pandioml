from abc import abstractmethod, ABCMeta, abstractproperty
from pandioml.model import ModelUtility
import signal
from functools import partial
import sys
import pickle


class FunctionBase(object, metaclass=ABCMeta):
    """Interface for Pandio Function"""
    model = abstractproperty()
    startup_ran = False
    id = None

    @abstractmethod
    def pipeline(self, input, context):
        raise NotImplementedError

    @classmethod
    def shutdown(cls, context=None):
        ModelUtility.upload(cls.id, cls.model, context)
        print("SHUTDOWN")

    @classmethod
    def startup(cls, context=None):
        if cls.startup_ran is False:
            print("STARTUP")
            cls.register_function(context=context)
            model = ModelUtility.download(cls.id, context)
            if model is not None:
                print("LOADED MODEL")
                cls.model = model

            # Only one signal can be registered, only register if this is not running inside of runner.py
            if sys.argv[0][-9:] != 'runner.py':
                signal.signal(signal.SIGINT, partial(cls.shutdown, context))
                signal.signal(signal.SIGTERM, partial(cls.shutdown, context))

            cls.startup_ran = True

    @classmethod
    def sync_models(cls, context=None):
        print("Download and combine models")
        fnc_state = context.get_state('fnc_state')
        if fnc_state is not None:
            print("Function state exists, proceeding")
            arr = pickle.loads(fnc_state)
            for model_file in arr:
                print(f"Processing {model_file}")
                if model_file != cls.id:
                    model = ModelUtility.download(model_file, context)
                    if model is not None:
                        print(f"Combining {model_file} with current model")
                        cls.model = ModelUtility.combine(cls.model, model)

    @classmethod
    def register_function(cls, context=None):
        fnc_state = context.get_state('fnc_state')
        if fnc_state is not None:
            arr = pickle.loads(fnc_state)
            if cls.id not in arr:
                arr.append(cls.id)

            context.put_state('fnc_state', pickle.dumps(arr, 0))
        else:
            context.put_state('fnc_state', pickle.dumps([cls.id], 0))

    @classmethod
    def fit(cls, result={}):
        cls.model.partial_fit(result['features'], result['labels'])
        return result

    @classmethod
    def predict(cls, result={}):
        result['predict'] = cls.model.predict(result['features'])
        return result

    @classmethod
    def error(cls, result={}):
        print(result)
        raise Exception('HALT!')

    @classmethod
    def output(cls, result={}):
        return result

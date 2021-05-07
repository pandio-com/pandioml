from abc import abstractmethod, ABCMeta, abstractproperty
import signal
import sys
import pickle
import codecs
from pandioml.model import numpy2dict, stream, ModelUtility
from pandioml.core.artifacts import artifact


class FunctionBase(object, metaclass=ABCMeta):
    """Interface for Pandio Function"""
    model = abstractproperty()
    startup_ran = False
    input = None
    storage = None
    config = None
    _result = None

    @classmethod
    def __init__(cls, input=None, context=None, config=None):
        cls.input = input
        cls.storage = Storage(context=context)
        cls.config = config

    @abstractmethod
    def pipelines(self):
        raise NotImplementedError

    @classmethod
    def get_result(self):
        return self._result

    @classmethod
    def set_result(self, result):
        self._result = result

    @classmethod
    def shutdown(cls):
        artifact.save()
        print("SHUTDOWN")

    @classmethod
    def startup(cls):
        if cls.startup_ran is False:
            print("STARTUP")
            cls.register_function()

            # TODO, Pulsar runs this in a child process, so these do not work
            # Only one signal can be registered, only register if this is not running inside of runner.py
            if 1 != 1 and sys.argv[0][-9:] != 'runner.py':
                signal.signal(signal.SIGINT, cls.shutdown)
                signal.signal(signal.SIGTERM, cls.shutdown)

            cls.startup_ran = True

    @classmethod
    def sync_models(cls):
        print("Download and combine models")
        fnc_state = cls.storage.get('fnc_state')
        if fnc_state is not None:
            print("Function state exists, proceeding")
            arr = pickle.loads(codecs.decode(fnc_state.encode(), "base64"))
            for model_file in arr:
                print(f"Processing {model_file}")
                if model_file != artifact.get_name_id():
                    model = ModelUtility.download(model_file, cls.storage)
                    if model is not None:
                        print(f"Combining {model_file} with current model")
                        cls.model = ModelUtility.combine(cls.model, model)

    @classmethod
    def register_function(cls):
        fnc_state = cls.storage.get('fnc_state')
        if fnc_state is not None:
            arr = pickle.loads(codecs.decode(fnc_state.encode(), "base64"))
            if artifact.get_name_id() not in arr:
                arr.append(artifact.get_name_id())

            cls.storage.set('fnc_state', codecs.encode(pickle.dumps(arr), "base64").decode())
        else:
            cls.storage.set('fnc_state', codecs.encode(pickle.dumps([artifact.get_name_id()]), "base64").decode())

    @classmethod
    def fit(cls, result={}):
        cls.model.learn_one(result['features'], result['labels'])
        return result

    @classmethod
    def predict(cls, result={}):
        result['prediction'] = cls.model.predict_one(result['features'])
        # Sometimes this returns a numpy.float64
        # TODO, dig into why
        if hasattr(result['prediction'], 'item'):
            result['prediction'] = result['prediction'].item()

        return result

    @classmethod
    def error(cls, result={}):
        print(result[0])
        print(result[1])
        #raise Exception(f"An exception occurred in the pipeline: {result[0]} {result[1]}")
        raise Exception("Halt!")


class Storage:
    context = None

    def __init__(self, context=None):
        self.context = context

    def set(self, key, value):
        return self.context.put_state(key, value)

    def get(self, key):
        return self.context.get_state(key)

    def increment_counter(self, key, amount):
        return None
        return self.context.increment_counter(key, amount)

    def delete_counter(self, key):
        return None
        return self.context.del_counter(key)

    def get_counter(self, key):
        return None
        return self.context.get_counter(key)

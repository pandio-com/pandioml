from abc import abstractmethod, ABCMeta, abstractproperty
from pandioml.model import ModelUtility
import signal
import sys
import pickle
import codecs


class FunctionBase(object, metaclass=ABCMeta):
    """Interface for Pandio Function"""
    model = abstractproperty()
    startup_ran = False
    id = None
    input = None
    storage = None

    @classmethod
    def __init__(cls, id=None, input=None, context=None):
        cls.id = id
        cls.input = input
        cls.storage = Storage(context=context)

    @abstractmethod
    def pipelines(self):
        raise NotImplementedError

    @classmethod
    def shutdown(cls):
        ModelUtility.upload(cls.id, cls.model, cls.storage)
        print("SHUTDOWN")

    @classmethod
    def startup(cls):
        if cls.startup_ran is False:
            print("STARTUP")
            cls.register_function()
            model = ModelUtility.download(cls.id, cls.storage)
            if model is not None:
                print("LOADED MODEL")
                cls.model = model

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
                if model_file != cls.id:
                    model = ModelUtility.download(model_file, cls.storage)
                    if model is not None:
                        print(f"Combining {model_file} with current model")
                        cls.model = ModelUtility.combine(cls.model, model)

    @classmethod
    def register_function(cls):
        fnc_state = cls.storage.get('fnc_state')
        if fnc_state is not None:
            arr = pickle.loads(codecs.decode(fnc_state.encode(), "base64"))
            if cls.id not in arr:
                arr.append(cls.id)

            cls.storage.set('fnc_state', codecs.encode(pickle.dumps(arr), "base64").decode())
        else:
            cls.storage.set('fnc_state', codecs.encode(pickle.dumps([cls.id]), "base64").decode())

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


class Storage:
    context = None

    def __init__(self, context=None):
        self.context = context

    def set(self, key, value):
        return None
        return self.context.put_state(key, value)

    def get(self, key):
        return None
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

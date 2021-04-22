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
    input_schema = abstractproperty()
    output_schema = abstractproperty()
    startup_ran = False
    input = None
    output = None
    storage = None
    config = None
    load_model = True

    @classmethod
    def __init__(cls, input=None, context=None, config=None):
        cls.input = input
        cls.storage = Storage(context=context)
        cls.config = config

    @abstractmethod
    def pipelines(self):
        raise NotImplementedError

    @classmethod
    def shutdown(cls):
        artifact.save()
        #ModelUtility.upload(artifact.get_name_id(), cls.model, cls.storage)
        print("SHUTDOWN")

    @classmethod
    def startup(cls):
        if cls.startup_ran is False:
            print("STARTUP")
            cls.register_function()
            #if cls.load_model is True:
            #    model = ModelUtility.download(artifact.get_name_id(), cls.storage)
            #    if model is not None:
            #        print("LOADED MODEL")
            #        cls.model = model

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
        for x, y in stream.iter_array(result['features'], result['labels']):
            cls.model.learn_one(x, y)
        return result

    @classmethod
    def predict(cls, result={}):
        result['prediction'] = cls.model.predict_one(numpy2dict(result['features'][0]))

        return result

    @classmethod
    def error(cls, result={}):
        print(result)
        raise Exception('HALT!')

    @classmethod
    def done(cls, result={}):
        return result


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

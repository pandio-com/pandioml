import pickle
import codecs
from river.utils import inspect, math, pretty, skmultiflow_utils
from river.utils.data_conversion import dict2numpy, numpy2dict
from river.utils.estimator_checks import check_estimator
from river.utils.histogram import Histogram
from river.utils.param_grid import expand_param_grid
from river.utils.sdft import SDFT
from river.utils.skyline import Skyline
from river.utils.window import SortedWindow, Window
import os

__all__ = [
    "check_estimator",
    "dict2numpy",
    "expand_param_grid",
    "inspect",
    "math",
    "pretty",
    "Histogram",
    "numpy2dict",
    "SDFT",
    "skmultiflow_utils",
    "Skyline",
    "SortedWindow",
    "Window",
    "ModelUtility"
]


class ModelUtility:
    @staticmethod
    def load_or_instantiate(path, model):
        if os.path.isfile(path):
            return pickle.loads(path)

        if callable(model):
            return model()

        return None

    @staticmethod
    def upload(model_name, model, storage):
        if model_name is not None:
            return storage.set(model_name, codecs.encode(pickle.dumps(model), "base64").decode())
        else:
            return False

    @staticmethod
    def download(model_name, storage):
        if model_name is not None:
            state = storage.get(model_name)
            if state is not None:
                return pickle.loads(codecs.decode(state.encode(), "base64"))

        return None

    @staticmethod
    def combine(model_a, model_b):
        #model_a.estimators_ += model_b.estimators_
        #model_a.n_estimators = len(model_a.estimators_)
        #return model_a
        return model_a

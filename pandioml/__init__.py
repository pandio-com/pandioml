import os
from . import model
from . import function
from . import data
from . import core
from . import metrics
from . import stats

__all__ = ['model', 'function', 'data', 'core', 'metrics', 'stats']


def requirements():
    f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt'), "r")
    return f.read().splitlines()

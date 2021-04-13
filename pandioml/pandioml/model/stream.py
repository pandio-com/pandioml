from river.stream.cache import Cache
from river.stream.iter_arff import iter_arff
from river.stream.iter_array import iter_array
from river.stream.iter_csv import iter_csv
from river.stream.iter_libsvm import iter_libsvm
from river.stream.qa import simulate_qa
from river.stream.shuffling import shuffle

__all__ = [
    "Cache",
    "iter_arff",
    "iter_array",
    "iter_csv",
    "iter_libsvm",
    "simulate_qa",
    "shuffle",
]

try:
    from .iter_pandas import iter_pandas

    __all__ += ["iter_pandas"]
except ImportError:
    pass

try:
    from .iter_sklearn import iter_sklearn_dataset

    __all__ += ["iter_sklearn_dataset"]
except ImportError:
    pass

try:
    from .iter_sql import iter_sql

    __all__ += ["iter_sql"]
except ImportError:
    pass

try:
    from .iter_vaex import iter_vaex

    __all__ += ["iter_vaex"]
except ImportError:
    pass
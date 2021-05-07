from river.reco.baseline import Baseline
from river.reco.biased_mf import BiasedMF
from river.reco.funk_mf import FunkMF
from river.reco.normal import RandomNormal

__all__ = ["Baseline", "BiasedMF", "FunkMF", "RandomNormal"]

try:
    from .surprise import SurpriseWrapper

    __all__ += ["SurpriseWrapper"]
except ImportError:
    pass

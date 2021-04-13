from river.expert.bandit import EpsilonGreedyRegressor, UCBRegressor
from river.expert.ewa import EWARegressor
from river.expert.sh import SuccessiveHalvingClassifier, SuccessiveHalvingRegressor
from river.expert.stacking import StackingClassifier

__all__ = [
    "EpsilonGreedyRegressor",
    "EWARegressor",
    "SuccessiveHalvingClassifier",
    "SuccessiveHalvingRegressor",
    "StackingClassifier",
    "UCBRegressor",
]
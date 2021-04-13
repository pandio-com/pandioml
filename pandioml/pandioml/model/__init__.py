# river
from .naive_bayes import GaussianNB, MultinomialNB, ComplementNB, BernoulliNB
from .anomaly_detection import HalfSpaceTrees
from .cluster import KMeans
from .ensemble import AdaptiveRandomForestClassifier, AdaptiveRandomForestRegressor, AdaBoostClassifier, \
    ADWINBaggingClassifier, BaggingClassifier, BaggingRegressor, LeveragingBaggingClassifier, SRPClassifier
from .evaluation import load_binary_clf_tracks, progressive_val_score, Track
from .expert import EpsilonGreedyRegressor, EWARegressor, SuccessiveHalvingClassifier, SuccessiveHalvingRegressor, \
    StackingClassifier, UCBRegressor
from .factor import FFMClassifier, FFMRegressor, FMClassifier, FMRegressor, FwFMClassifier, FwFMRegressor, \
    HOFMClassifier, HOFMRegressor
from .feature_extraction import Agg, TargetAgg, RBFSampler, PolynomialExtender, TFIDF, BagOfWords
from .feature_selection import SelectKBest, PoissonInclusion, VarianceThreshold
from .imblearn import HardSamplingClassifier, HardSamplingRegressor, RandomOverSampler, RandomSampler, RandomUnderSampler
from .linear import ALMAClassifier, LinearRegression, LogisticRegression, Perceptron, PAClassifier, PARegressor, \
    SoftmaxRegression
from .meta import PredClipper, BoxCoxRegressor, TransformedTargetRegressor
from .multiclass import OutputCodeClassifier, OneVsOneClassifier, OneVsRestClassifier
from .multioutput import ClassifierChain, MonteCarloClassifierChain, ProbabilisticClassifierChain, \
    RegressorChain
from .neighbors import KNNADWINClassifier, KNNClassifier, KNNRegressor, SAMKNNClassifier
from .neural_network import activations, MLPRegressor
from .optim import losses, initializers, schedulers ,AdaBound, AdaDelta, AdaGrad, AdaMax, Adam, AMSGrad, Averager, \
    Optimizer, FTRLProximal, Momentum, Nadam, NesterovMomentum, RMSProp, SGD
from .preprocessing import FeatureHasher, PreviousImputer, StatImputer, LDA, OneHotEncoder, \
    AdaptiveStandardScaler, Binarizer, MaxAbsScaler, MinMaxScaler, Normalizer, RobustScaler, StandardScaler
from .proba import Gaussian, Multinomial
from .reco import Baseline, BiasedMF, FunkMF, RandomNormal
from .stats import AutoCorr, Bivariate, Univariate, Count, Cov, RollingCov, Entropy, EWMean, EWVar, IQR, RollingIQR, \
    Kurtosis, Link, AbsMax, Max, RollingAbsMax, RollingMax, BayesianMean, Mean, RollingMean, Min, RollingMin, Mode, \
    RollingMode, NUnique, PearsonCorr, RollingPearsonCorr, PeakToPeak, RollingPeakToPeak, Quantile, RollingQuantile, \
    SEM, RollingSEM, Shift, Skew, RollingSum, Sum, RollingVar, Var
from .stream import Cache, iter_arff, iter_array, iter_csv, iter_libsvm, simulate_qa, shuffle
from .time_series import Detrender, GroupDetrender, SNARIMAX
from .trees import splitter, ExtremelyFastDecisionTreeClassifier, HoeffdingAdaptiveTreeClassifier, \
    HoeffdingAdaptiveTreeRegressor, HoeffdingTreeClassifier, HoeffdingTreeRegressor, iSOUPTreeRegressor, \
    LabelCombinationHoeffdingTreeClassifier
from .utility import inspect, math, pretty, skmultiflow_utils, dict2numpy, numpy2dict, check_estimator, Histogram, \
    expand_param_grid, SDFT, Skyline, SortedWindow, Window

# scikit-multiflow
from .drift_detection import ADWIN, DDM, EDDM, HDDM_A, HDDM_W, KSWIN, PageHinkley
from .prototype import RobustSoftLearningVectorQuantization
from .rules import VeryFastDecisionRulesClassifier
from .transform import MissingValuesCleaner, OneHotToCategorical, WindowedMinmaxScaler, WindowedStandardScaler
from .evaluation import EvaluateHoldout, EvaluatePrequential, EvaluatePrequentialDelayed
from .trees import HoeffdingTreeClassifier, HoeffdingAdaptiveTreeClassifier, \
    ExtremelyFastDecisionTreeClassifier, LabelCombinationHoeffdingTreeClassifier, HoeffdingTreeRegressor, \
    HoeffdingAdaptiveTreeRegressor, iSOUPTreeRegressor, StackedSingleTargetHoeffdingTreeRegressor
from .lazy import KNNClassifier, KNNADWINClassifier, SAMKNNClassifier, KNNRegressor
from .meta import AccuracyWeightedEnsembleClassifier, AdditiveExpertEnsembleClassifier, BatchIncrementalClassifier, ClassifierChain, \
    ProbabilisticClassifierChain, MonteCarloClassifierChain, DynamicWeightedMajorityClassifier, LearnPPNSEClassifier, \
    LearnPPClassifier, MultiOutputLearner, OnlineAdaC2Classifier, \
    OnlineBoostingClassifier, OnlineCSB2Classifier, OnlineRUSBoostClassifier, OnlineSMOTEBaggingClassifier, \
    OnlineUnderOverBaggingClassifier, OzaBaggingClassifier, OzaBaggingADWINClassifier, RegressorChain, \
    StreamingRandomPatchesClassifier

# Pandio
from .utility import ModelUtility

__all__ = ["GaussianNB", "MultinomialNB", "ComplementNB", "BernoulliNB", "ModelUtility", "KNNClassifier", "KNNADWINClassifier",
           "SAMKNNClassifier", "KNNRegressor", "HoeffdingTreeClassifier", "HoeffdingAdaptiveTreeClassifier",
           "ExtremelyFastDecisionTreeClassifier", "LabelCombinationHoeffdingTreeClassifier", "HoeffdingTreeRegressor",
           "HoeffdingAdaptiveTreeRegressor", "iSOUPTreeRegressor", "StackedSingleTargetHoeffdingTreeRegressor",
           "AccuracyWeightedEnsembleClassifier", "AdaptiveRandomForestClassifier",
           "AdaptiveRandomForestRegressor", "AdditiveExpertEnsembleClassifier", "BatchIncrementalClassifier", "ClassifierChain",
           "ProbabilisticClassifierChain", "MonteCarloClassifierChain", "DynamicWeightedMajorityClassifier", "LearnPPNSEClassifier",
           "LearnPPClassifier", "LeveragingBaggingClassifier", "MultiOutputLearner", "OnlineAdaC2Classifier",
           "OnlineBoostingClassifier", "OnlineCSB2Classifier", "OnlineRUSBoostClassifier", "OnlineSMOTEBaggingClassifier",
           "OnlineUnderOverBaggingClassifier", "OzaBaggingClassifier", "OzaBaggingADWINClassifier", "RegressorChain",
           "StreamingRandomPatchesClassifier", "PerceptronMask", "RobustSoftLearningVectorQuantization",
           "VeryFastDecisionRulesClassifier", "ADWIN", "DDM", "EDDM", "HDDM_A", "HDDM_W", "KSWIN", "PageHinkley",
           "EvaluateHoldout", "EvaluatePrequential", "EvaluatePrequentialDelayed", "MissingValuesCleaner",
           "OneHotToCategorical", "WindowedMinmaxScaler", "WindowedStandardScaler", "HalfSpaceTrees", "KMeans",
           "AdaptiveRandomForestClassifier", "AdaptiveRandomForestRegressor", "AdaBoostClassifier",
           "ADWINBaggingClassifier", "BaggingClassifier", "BaggingRegressor", "LeveragingBaggingClassifier",
           "SRPClassifier", "load_binary_clf_tracks", "progressive_val_score", "Track", "EpsilonGreedyRegressor",
           "EWARegressor", "SuccessiveHalvingClassifier", "SuccessiveHalvingRegressor", "StackingClassifier",
           "UCBRegressor", "FFMClassifier", "FFMRegressor", "FMClassifier", "FMRegressor", "FwFMClassifier",
           "FwFMRegressor", "HOFMClassifier", "HOFMRegressor", "Agg", "BagOfWords", "PolynomialExtender", "RBFSampler",
           "TargetAgg", "TFIDF", "PoissonInclusion", "SelectKBest", "VarianceThreshold", "HardSamplingClassifier",
           "HardSamplingRegressor", "RandomOverSampler", "RandomUnderSampler", "RandomSampler", "ALMAClassifier",
           "LinearRegression", "LogisticRegression", "PAClassifier", "PARegressor", "Perceptron", "SoftmaxRegression",
           "BoxCoxRegressor", "PredClipper", "TransformedTargetRegressor", "OutputCodeClassifier", "OneVsOneClassifier",
           "OneVsRestClassifier", "ClassifierChain", "MonteCarloClassifierChain", "ProbabilisticClassifierChain",
           "RegressorChain", "KNNADWINClassifier", "KNNClassifier", "KNNRegressor", "SAMKNNClassifier", "activations",
           "MLPRegressor", "AdaBound", "AdaDelta" ,"AdaGrad", "Adam", "AMSGrad", "AdaMax", "Averager", "FTRLProximal",
           "initializers", "losses", "Momentum", "Nadam", "NesterovMomentum", "Optimizer", "RMSProp", "schedulers",
           "SGD", "AdaptiveStandardScaler", "Binarizer", "FeatureHasher", "LDA", "MaxAbsScaler", "MinMaxScaler",
           "Normalizer", "OneHotEncoder", "PreviousImputer", "RobustScaler", "StandardScaler", "StatImputer",
           "Gaussian", "Multinomial", "Baseline", "BiasedMF", "FunkMF", "RandomNormal", "AbsMax", "AutoCorr",
           "BayesianMean", "Bivariate", "Count", "Cov", "Entropy", "EWMean", "EWVar", "IQR", "Kurtosis", "Link", "Max",
           "Mean", "Min", "Mode", "NUnique", "PeakToPeak", "PearsonCorr", "Quantile", "RollingAbsMax", "RollingCov",
           "RollingIQR", "RollingMax", "RollingMean", "RollingMin", "RollingMode", "RollingPeakToPeak",
           "RollingPearsonCorr", "RollingQuantile", "RollingSEM", "RollingSum", "RollingVar", "SEM", "Shift", "Skew",
           "Sum", "Univariate", "Var", "Cache", "iter_arff", "iter_array", "iter_csv", "iter_libsvm", "simulate_qa",
           "shuffle", "Detrender", "GroupDetrender", "SNARIMAX", "splitter", "check_estimator", "dict2numpy",
           "expand_param_grid", "inspect", "math", "pretty", "Histogram", "numpy2dict", "SDFT", "skmultiflow_utils",
           "Skyline", "SortedWindow", "Window"]

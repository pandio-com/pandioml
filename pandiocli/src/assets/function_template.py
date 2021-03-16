import numpy as np
from pandioml.function import FunctionInterface


class Fnc(FunctionInterface):
    model = None

    def __init__(self, model):
        self.model = model

    # return an np.array with the features
    def feature_extraction(self, input):
        return np.array()

    # return an np.array with the labels
    def label_extraction(self, input):
        return np.array()

    def fit(self, features, labels):
        self.model.partial_fit(features, labels)

    def predict(self, features):
        return self.model.predict(features)

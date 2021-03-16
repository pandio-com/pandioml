import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import HashingVectorizer
from pandioml.function import FunctionInterface


class Fnc(FunctionInterface):
    model = None

    def __init__(self, model):
        self.model = model
        self.vectorizer = HashingVectorizer(n_features=20)

    def label_extraction(self, input):
        if 'yahoo' in input['email'] or 'hotmail' in input['email']:
            return np.array([1])
        else:
            return np.array([0])

    def feature_extraction(self, input):
        length = len(input) + 27

        data = np.zeros([1, length])

        index = 0
        for key in input:
            if key == 'email':
                hash_list = self.vectorizer.transform([input[key]]).toarray()
                for h in range(len(hash_list[0])):
                    data[0, index] = hash_list[0][h]
                    index += 1
            elif key == 'ip':
                ip_list = input[key].split(".")[:4]
                for h in range(len(ip_list)):
                    data[0, index] = ip_list[h]
                    index += 1
            elif key == 'timestamp':
                data[0, index] = input[key]
                index += 1
                timestamp_formatted = pd.to_datetime(input[key], unit='s')
                data[0, index] = timestamp_formatted.dayofweek
                index += 1
                data[0, index] = 1 if (timestamp_formatted.dayofweek // 5 == 1) else 0
                index += 1
                data[0, index] = timestamp_formatted.month
                index += 1
                data[0, index] = timestamp_formatted.day
                index += 1
                data[0, index] = timestamp_formatted.hour
                index += 1

        return data

    def fit(self, features, labels):
        self.model.partial_fit(features, labels)

    def predict(self, features):
        return self.model.predict(features)

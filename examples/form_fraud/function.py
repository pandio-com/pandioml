from pandioml.model import NaiveBayes
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import HashingVectorizer
from pandioml.function import FunctionBase
from pandioml.core import Pipeline


class Fnc(FunctionBase):
    model = NaiveBayes()

    def __init__(self, id):
        if id is None:
            self.id = f"example1.model"
        else:
            self.id = id
        self.vectorizer = HashingVectorizer(n_features=20)

    def pipeline(self, *args, **kwargs):
        return Pipeline(*args, **kwargs) \
            .then(self.label_extraction, input=kwargs['input']) \
            .then(self.feature_extraction, input=kwargs['input']) \
            .then(self.fit) \
            .final(self.predict) \
            .done(self.output) \
            .catch(self.error)

    def label_extraction(self, input=None, result={}):
        if 'yahoo' in input.email or 'hotmail' in input.email:
            result['labels'] = np.array([1])
        else:
            result['labels'] = np.array([0])

        return result

    def feature_extraction(self, input=None, result={}):
        #raise Exception("Forcing an error")

        length = len(input.__dict__) + 27

        data = np.zeros([1, length])

        index = 0
        for key in input.__dict__.keys():
            if key == 'email':
                hash_list = self.vectorizer.transform([getattr(input, key)]).toarray()
                for h in range(len(hash_list[0])):
                    data[0, index] = hash_list[0][h]
                    index += 1
            elif key == 'ip':
                ip_list = getattr(input, key).split(".")[:4]
                for h in range(len(ip_list)):
                    data[0, index] = ip_list[h]
                    index += 1
            elif key == 'timestamp':
                data[0, index] = getattr(input, key)
                timestamp_formatted = pd.to_datetime(data[0, index], unit='s')
                index += 1
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

        result['features'] = data
        return result

from pandioml.model import GaussianNB
from pandioml.model import HoeffdingTreeClassifier
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import HashingVectorizer
from pandioml.function import FunctionBase
from pandioml.core import Pipeline, Pipelines
from pandioml.data.record import JsonSchema, Record, String, Integer
from pandioml.data import Submission


class SubmissionPrediction(Record):
    email = String()
    ip = String()
    timestamp = Integer()
    prediction = Integer()


class Fnc(FunctionBase):
    model = GaussianNB()
    input_schema = JsonSchema(Submission)
    output_schema = JsonSchema(SubmissionPrediction)

    def pipelines(self, *args, **kwargs):
        return Pipelines().add(
            'inference',
            Pipeline(*args, **kwargs)
                .then(self.label_extraction)
                .then(self.feature_extraction)
                .then(self.fit)
                .final(self.predict)
                .done(self.output)
                .catch(self.error)
        ).add(
            'drift',
            Pipeline(*args, **kwargs)
                .then(self.detect_drift)
                .done(self.output)
                .catch(self.error)
        ).add(
            'evaluate',
            Pipeline(*args, **kwargs)
                .then(self.evaluate)
                .done(self.output)
                .catch(self.error)
        ).add(
            'inference_tree',
            Pipeline(*args, **kwargs)
                .then(self.set_model, HoeffdingTreeClassifier)
                .then(self.label_extraction)
                .then(self.feature_extraction)
                .then(self.fit)
                .final(self.predict)
                .done(self.output)
                .catch(self.error)
        )

    def output(self, result={}):
        self.output = SubmissionPrediction(email=self.input.email, ip=self.input.ip, timestamp=self.input.timestamp)
        if hasattr(self.model, 'partial_fit'):
            self.output.prediction = result['prediction'][0].item()
        elif hasattr(self.model, 'learn_one'):
            self.output.prediction = result['prediction'].item()
        return result

    def set_model(self, model):
        self.model = model

    def detect_drift(self, result={}):
        result['drift'] = False

        return result

    def evaluate(self, result={}):
        result['precision'] = 0

        return result

    def label_extraction(self, result={}):
        if 'yahoo' in self.input.email or 'hotmail' in self.input.email:
            result['labels'] = np.array([1])
        else:
            result['labels'] = np.array([0])

        return result

    def feature_extraction(self, result={}):
        #raise Exception("Forcing an error")

        vectorizer = HashingVectorizer(n_features=20)

        length = len(self.input.__dict__) + 27

        data = np.zeros([1, length])

        index = 0
        for key in self.input.__dict__.keys():
            if key == 'email':
                hash_list = vectorizer.transform([getattr(self.input, key)]).toarray()
                for h in range(len(hash_list[0])):
                    data[0, index] = hash_list[0][h]
                    index += 1
            elif key == 'ip':
                ip_list = getattr(self.input, key).split(".")[:4]
                for h in range(len(ip_list)):
                    data[0, index] = ip_list[h]
                    index += 1
            elif key == 'timestamp':
                data[0, index] = getattr(self.input, key)
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

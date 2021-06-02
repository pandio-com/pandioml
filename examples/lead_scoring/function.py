from pandioml.model import AdaptiveRandomForestClassifier
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import HashingVectorizer
from pandioml.function import FunctionBase
from pandioml.core import Pipeline, Pipelines
from pandioml.data.record import Record, String, Integer, JsonSchema
from pandioml.model import StandardScaler
from pandioml.core.artifacts import artifact
from pandioml.metrics import Accuracy, Precision, Recall, ConfusionMatrix


class Submission(Record):
    name = String()
    email = String()
    ip = String()
    timestamp = Integer()


class SubmissionPrediction(Record):
    name = String()
    email = String()
    ip = String()
    timestamp = Integer()
    prediction = Integer()


class Function(FunctionBase):
    model = artifact.add('AdaptiveRandomForestClassifier_model', AdaptiveRandomForestClassifier(
        n_models=3,
        seed=42
    ))
    input_schema = JsonSchema(Submission)
    scaler = StandardScaler()
    vectorizer = HashingVectorizer(n_features=8)
    accuracy = Accuracy()
    precision = Precision()
    recall = Recall()
    confusion_matrix = ConfusionMatrix()

    def pipelines(self, *args, **kwargs):
        return Pipelines().add(
            'inference',
            Pipeline(*args, **kwargs)
                .then(self.feature_extraction)
                .then(self.scale)
                .then(self.label_extraction)
                .then(self.fit)
                .final(self.predict)
                .done(self.done)
                .catch(self.error)
        ).add(
            'inference_wo_scale',
            Pipeline(*args, **kwargs)
                .then(self.feature_extraction)
                #.then(self.scale)
                .then(self.label_extraction)
                .then(self.fit)
                .final(self.predict)
                .done(self.done)
                .catch(self.error)
        )

    def done(self, result={}):
        self.accuracy = artifact.add('Accuracy_Metric', self.accuracy.update(result['labels'], result['prediction']))
        self.precision = artifact.add('Precision_Metric', self.precision.update(result['labels'], result['prediction']))
        self.recall = artifact.add('Recall_Metric', self.recall.update(result['labels'], result['prediction']))
        self.confusion_matrix = artifact.add('Confusion_Matrix_Metric', self.confusion_matrix.update(result['labels'],
                                                                                                     result[
                                                                                                         'prediction']))
        print(self.accuracy)
        print(self.precision)
        print(self.recall)
        print(self.confusion_matrix)
        return SubmissionPrediction(name=self.input.name, email=self.input.email, ip=self.input.ip,
                                    timestamp=self.input.timestamp, prediction=result['prediction'])

    def scale(self, result={}):
        result['features'] = self.scaler.learn_one(result['features']).transform_one(result['features'])
        return result

    def label_extraction(self, result={}):
        result['labels'] = 1 if 'yahoo' in self.input.email or 'hotmail' in self.input.email else 0
        return result

    def feature_extraction(self, result={}):
        data = []

        _hash = self.vectorizer.transform([getattr(self.input, 'name')]).toarray()
        data.extend(_hash[0])

        _hash = self.vectorizer.transform([getattr(self.input, 'email')]).toarray()
        data.extend(_hash[0])

        _split = getattr(self.input, 'email').split('@')
        _hash = self.vectorizer.transform([_split[0]]).toarray()
        data.extend(_hash[0])
        _hash = self.vectorizer.transform([_split[1]]).toarray()
        data.extend(_hash[0])

        regex = re.compile('[^a-zA-Z]')
        # The name and email being similar is a good sign
        data.append(float(self.levenshtein(regex.sub('', _split[0]), regex.sub('', getattr(self.input, 'name')))))

        ip_list = getattr(self.input, 'ip').split(".")[:4]
        for h in range(len(ip_list)):
            data.append(int(ip_list[h]))

        data.append(getattr(self.input, 'timestamp'))
        timestamp_formatted = pd.to_datetime(getattr(self.input, 'timestamp'), unit='s')
        data.append(timestamp_formatted.dayofweek)
        data.append(1 if (timestamp_formatted.dayofweek // 5 == 1) else 0)
        data.append(timestamp_formatted.month)
        data.append(timestamp_formatted.day)
        data.append(timestamp_formatted.hour)

        # Set as a dict
        result['features'] = {k: v for k, v in enumerate(data)}

        return result

    @staticmethod
    def levenshtein(seq1, seq2):
        size_x = len(seq1) + 1
        size_y = len(seq2) + 1
        matrix = np.zeros((size_x, size_y))
        for x in range(size_x):
            matrix[x, 0] = x
        for y in range(size_y):
            matrix[0, y] = y

        for x in range(1, size_x):
            for y in range(1, size_y):
                if seq1[x - 1] == seq2[y - 1]:
                    matrix[x, y] = min(
                        matrix[x - 1, y] + 1,
                        matrix[x - 1, y - 1],
                        matrix[x, y - 1] + 1
                    )
                else:
                    matrix[x, y] = min(
                        matrix[x - 1, y] + 1,
                        matrix[x - 1, y - 1] + 1,
                        matrix[x, y - 1] + 1
                    )

        return (matrix[size_x - 1, size_y - 1])

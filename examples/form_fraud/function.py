from pandioml.model import GaussianNB
import pandas as pd
from sklearn.feature_extraction.text import HashingVectorizer
from pandioml.function import FunctionBase
from pandioml.core import Pipeline, Pipelines
from pandioml.data.record import Record, String, Integer
from pandioml.model import StandardScaler
from pandioml.core.artifacts import artifact


class SubmissionPrediction(Record):
    email = String()
    ip = String()
    timestamp = Integer()
    prediction = Integer()


class Function(FunctionBase):
    model = artifact.add('GaussianNB_model', GaussianNB())
    scaler = StandardScaler()
    vectorizer = HashingVectorizer(n_features=20)

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
        )

    def done(self, result={}):
        output = SubmissionPrediction(email=self.input.email, ip=self.input.ip, timestamp=self.input.timestamp)
        output.prediction = result['prediction']
        return output

    def scale(self, result={}):
        result['features'] = self.scaler.learn_one(result['features']).transform_one(result['features'])
        return result

    def label_extraction(self, result={}):
        result['labels'] = 1 if 'yahoo' in self.input.email or 'hotmail' in self.input.email else 0
        return result

    def feature_extraction(self, result={}):
        data = []

        _hash = self.vectorizer.transform([getattr(self.input, 'email')]).toarray()
        data.extend(_hash[0])

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

from pandioml.function import FunctionBase
from pandioml.core import Pipeline, Pipelines
from pandioml.data.record import JsonSchema, String, Float, Boolean, Double, Integer, Record
from pandioml.data import RestaurantDay
import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer
from pandioml.core import interact
from pandioml.model import GaussianNB
from pandioml.model import LinearRegression
from pandioml.model import LogisticRegression
from pandioml.model import Perceptron
from pandioml.core.artifacts import artifact


class RestaurantDayOutput(Record):
    store_id = String()
    timestamp = Float()
    is_holiday = Boolean()
    genre_name = String()
    area_name = String()
    latitude = Double()
    longitude = Double()
    visitors = Integer()
    prediction = Float()


class Fnc(FunctionBase):
    model = artifact.add('model', GaussianNB())
    load_model = False
    input_schema = JsonSchema(RestaurantDay)
    output_schema = JsonSchema(RestaurantDayOutput)

    def done(self, result={}):
        self.output = RestaurantDayOutput(**self.input._get_fields)
        self.output.prediction = result['prediction']
        return result

    def feature_extraction(self, result={}):
        vectorizer = HashingVectorizer(n_features=8)

        data = []

        data.append(self.input.is_holiday)
        data.append(self.input.longitude)
        data.append(self.input.latitude)
        data.append(self.input.timestamp)

        hash = vectorizer.transform([self.input.store_id]).toarray()
        data.extend(hash[0])

        hash = vectorizer.transform([self.input.genre_name]).toarray()
        data.extend(hash[0])

        hash = vectorizer.transform([self.input.area_name]).toarray()
        data.extend(hash[0])

        result['features'] = np.array([data])

        return result

    def label_extraction(self, result={}):
        result['labels'] = np.array([self.input.visitors])

        return result

    def pipelines(self, *args, **kwargs):
        return Pipelines().add(
            'inference',
            Pipeline(*args, **kwargs)
                .then(self.feature_extraction)
                .then(self.label_extraction)
                .then(self.fit)
                .final(self.predict)
                .done(self.done)
                .catch(self.error)
        )

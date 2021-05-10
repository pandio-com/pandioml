from pandioml.function import FunctionBase
from pandioml.core import Pipeline, Pipelines
from pandioml.data.record import String, Float, Boolean, Double, Integer, Record
from sklearn.feature_extraction.text import HashingVectorizer
from pandioml.model import GaussianNB
from pandioml.model import LinearRegression
from pandioml.model import LogisticRegression
from pandioml.model import Perceptron
from pandioml.core.artifacts import artifact
from pandioml.model import StandardScaler
from pandioml.model import ModelUtility


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


class Function(FunctionBase):
    model = artifact.add('LinearRegression_model',
                         ModelUtility.load_or_instantiate('LinearRegression_model.pickle', LinearRegression))
    scaler = StandardScaler()

    def done(self, result={}):
        output = RestaurantDayOutput(**dict((lambda x: (x, getattr(self.input, x)))(key) for key in
                                                 self.input._fields.keys()))

        output.prediction = result['prediction']

        return output

    def feature_extraction(self, result={}):
        vectorizer = HashingVectorizer(n_features=8)

        data = []

        data.append(0 if self.input.is_holiday else 0)
        data.append(self.input.longitude)
        data.append(self.input.latitude)
        data.append(self.input.timestamp)

        _hash = vectorizer.transform([self.input.store_id]).toarray()
        data.extend(_hash[0])

        _hash = vectorizer.transform([self.input.genre_name]).toarray()
        data.extend(_hash[0])

        _hash = vectorizer.transform([self.input.area_name]).toarray()
        data.extend(_hash[0])

        # Set as a dict
        result['features'] = {k: v for k, v in enumerate(data)}

        return result

    def label_extraction(self, result={}):
        result['labels'] = self.input.visitors

        return result

    def scale(self, result={}):
        result['features'] = self.scaler.learn_one(result['features']).transform_one(result['features'])
        return result

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

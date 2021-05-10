from pandioml.function import FunctionBase
from pandioml.core import Pipeline, Pipelines
from pandioml.data.record import String, Float, Integer, Record
from sklearn.feature_extraction.text import HashingVectorizer
from pandioml.model import LinearRegression
from pandioml.core.artifacts import artifact
from pandioml.model import StandardScaler
import pandas as pd


class MovieRatingOutput(Record):
    user_id = Integer()
    item_id = Integer()
    timestamp = Integer()
    title = String()
    release_date = Integer()
    genres = String()
    user_age = Integer()
    user_gender = String()
    user_occupation = String()
    user_zip_code = String()
    prediction = Float()


class Function(FunctionBase):
    model = artifact.add('LinearRegression_model', LinearRegression())
    scaler = StandardScaler()
    vectorizer = HashingVectorizer(n_features=8)

    def done(self, result={}):
        output = MovieRatingOutput(**dict((lambda x: (x, getattr(self.input, x)))(key) for key in
                                                 self.input._fields.keys()))

        output.prediction = result['prediction']

        return output

    def feature_extraction(self, result={}):
        data = []

        data.append(self.input.user_id)
        data.append(self.input.item_id)
        data.append(self.input.timestamp)
        timestamp_formatted = pd.to_datetime(self.input.timestamp)
        data.append(timestamp_formatted.dayofweek)
        data.append(1 if (timestamp_formatted.dayofweek // 5 == 1) else 0)
        data.append(timestamp_formatted.month)
        data.append(timestamp_formatted.day)
        data.append(timestamp_formatted.hour)
        data.append(self.input.release_date)
        timestamp_formatted = pd.to_datetime(self.input.release_date)
        data.append(timestamp_formatted.dayofweek)
        data.append(1 if (timestamp_formatted.dayofweek // 5 == 1) else 0)
        data.append(timestamp_formatted.month)
        data.append(timestamp_formatted.day)
        data.append(timestamp_formatted.hour)
        data.append(self.input.user_age)
        data.append(0 if self.input.user_gender is 'M' else 1)

        _hash = self.vectorizer.transform([self.input.title]).toarray()
        data.extend(_hash[0])

        _hash = self.vectorizer.transform([self.input.genres]).toarray()
        data.extend(_hash[0])

        _hash = self.vectorizer.transform([self.input.user_occupation]).toarray()
        data.extend(_hash[0])

        _hash = self.vectorizer.transform([self.input.user_zip_code]).toarray()
        data.extend(_hash[0])

        # Set as a dict
        result['features'] = {k: v for k, v in enumerate(data)}

        return result

    def label_extraction(self, result={}):
        result['labels'] = self.input.user_movie_rating

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

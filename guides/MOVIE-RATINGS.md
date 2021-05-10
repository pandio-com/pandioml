# Movie Ratings

This example is found in [./examples/movie_ratings](./examples/movie_ratings) and attempts to guess the rating a user will give to a movie.

## Install

It is highly recommended to setup a virtual environment before installing PandioML.

This is an optional step before getting started.

`python3 -m venv /path/to/new/virtual/environment`

`pip install pandioml pandiocli`

## Generate Project Template

`pandiocli function generate --project_folder test_function`

## Open Template File In Your Editor Of Choice

Let us create a model that attempts to guess the number of visitors that a restaurant will receive in a day based on the `RestaurantVisitorsDataset`

This dataset has the following schema:

```buildoutcfg
class MovieRating(Record):
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
    user_movie_rating = Float()
```

In your editor, you will see these methods that need to be defined:

* `pipelines`
* `feature_extraction`
* `label_extraction`
* `done`

Everything starts with the `pipelines` method. This is the method that gets called. It should return the pipelines that you wish to run.

```buildoutcfg
Pipelines().add(
    'inference',
    Pipeline(*args, **kwargs)
        .then(self.feature_extraction)
        .then(self.label_extraction)
        .then(self.fit)
        .final(self.predict)
        .done(self.done)
        .catch(self.error)
)
```

The above pipeline is provided for you. It executes 6 steps, three of which are defined by you, three are defined for you through the base class. You can overwrite them if you would like.

For more information on pipelines, please read our full documentation.

Next, lets handle **label_extraction**.

Here we are going to say if the email has hotmail or yahoo in it, it is fraud, otherwise not fraud. You can change this to be anything you would like.

```buildoutcfg
def label_extraction(self, result={}):
    result['labels'] = self.input.user_movie_rating
    return result
```

Next, lets look at the **feature_extraction**. This is where the fun begins.

This function can do anything you'd like, all it needs to return is the features as a dictionary.

```buildoutcfg
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
```

Lets break this down.

The first thing we do is create a vectorizer from the `sklearn.feature_extraction.text` module. This is a great function to turn a string into numbers. The number of numbers used to represent a string is defined by `n_features`. The more the better, but remember, performance will suffer the more features you have.

Next, we're just going to use a plain Python array, so we don't have to define the numpy array shape if we were to use a numpy array. This makes it a bit easier to add and remove features a little faster.

The rest is pretty straightforward. An array is being built by the values found in `self.input`.

Next, we have one important property we need to define.

This is the `model` property. Let us try a `LinearRegression` model.

Let us import it: `from pandioml.model import LinearRegression`

Now, we set the model property to the model:

```buildoutcfg
class Function(FunctionBase):
    model = LinearRegression()
```

Lastly we need to define the output. The output typically contains the prediction. Type safety is as important for the input as it is for the output that is going to be processed.

For this, you'll want to define a new class inside of the `function.py` file.

In this example, we'll use all the fields from the input, but add one more field for the prediction.

```buildoutcfg
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
```

As you can see, a single field was added to the end, that will contain our prediction.

Now that the class is defined, we can add the `output` method that uses this class.

```buildoutcfg
def done(self, result={}):
    output = MovieRatingOutput(**dict((lambda x: (x, getattr(self.input, x)))(key) for key in
                                                 self.input._fields.keys()))

    output.prediction = result['prediction']

    return output
```

Done! Now you can continue to test your pipeline in the next step.

## Test Your Pipeline

`pandiocli test --project_folder test_function --dataset_name MovieRatingDataset --loops 1000`

## Deploy Your Pipeline

`pandiocli function upload --project_folder test_function`

## Full Example Code

```buildoutcfg
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

```

# Form Submission Fraud

This example is found in [./examples/form_fraud](./examples/form_fraud) and simulates website form submissions that contain fraud.

## Install

It is highly recommended to setup a virtual environment before installing PandioML.

This is an optional step before getting started.

`python3 -m venv /path/to/new/virtual/environment`

`pip install pandioml pandiocli`

## Generate Project Template

`pandiocli function generate --project_name test_function`

## Open Template File In Your Editor Of Choice

Let us create a model that attempts to guess the number of visitors that a restaurant will receive in a day based on the `RestaurantVisitorsDataset`

This dataset has the following schema:

```buildoutcfg
class Submission(Record):
    email = String()
    ip = String()
    timestamp = Integer()
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
    result['labels'] = 1 if 'yahoo' in self.input.email or 'hotmail' in self.input.email else 0
    return result
```

Next, lets look at the **feature_extraction**. This is where the fun begins.

This function can do anything you'd like, all it needs to return is the features as a dictionary.

```buildoutcfg
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
```

Lets break this down.

The first thing we do is create a vectorizer from the `sklearn.feature_extraction.text` module. This is a great function to turn a string into numbers. The number of numbers used to represent a string is defined by `n_features`. The more the better, but remember, performance will suffer the more features you have.

Next, we're just going to use a plain Python array, so we don't have to define the numpy array shape if we were to use a numpy array. This makes it a bit easier to add and remove features a little faster.

The rest is pretty straightforward. An array is being built by the values found in `self.input`.

Next, we have one important property we need to define.

This is the `model` property. Let us try a `GaussianNB` model.

Let us import it: `from pandioml.model import GaussianNB`

Now, we set the model property to the model:

```buildoutcfg
class Function(FunctionBase):
    model = GaussianNB()
```

Lastly we need to define the output. The output typically contains the prediction. Type safety is as important for the input as it is for the output that is going to be processed.

For this, you'll want to define a new class inside of the `function.py` file.

In this example, we'll use all the fields from the input, but add one more field for the prediction.

```buildoutcfg
class SubmissionPrediction(Record):
    email = String()
    ip = String()
    timestamp = Integer()
    prediction = Integer()
```

As you can see, a single field was added to the end, that will contain our prediction.

Now that the class is defined, we can add the `output` method that uses this class.

```buildoutcfg
def done(self, result={}):
    output = SubmissionPrediction(email=self.input.email, ip=self.input.ip, timestamp=self.input.timestamp)
    output.prediction = result['prediction']
    return output
```

Done! Now you can continue to test your pipeline in the next step.

## Test Your Pipeline

`pandiocli test --project_folder test_function --dataset_name FormSubmissionGenerator --loops 1000`

## Deploy Your Pipeline

`pandiocli function upload --project_folder test_function`

## Full Example Code

```buildoutcfg
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

```
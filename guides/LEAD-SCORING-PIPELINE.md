# Lead Scoring Pipeline

This example is found in [./examples/lead_scoring](./examples/lead_scoring) and attempts to classify a lead as having a specific type of email (hotmail or yahoo).

## Install

It is highly recommended to setup a virtual environment before installing PandioML.

This is an optional step before getting started.

`python -m venv /path/to/new/virtual/environment`

`pip install pandioml`

## Generate Project Template

`pandiocli function generate --project_name lead_scoring`

## Open Template File In Your Editor Of Choice

Let us create a model that attempts to predict if a lead has a specific email type based on the dataset `examples/lead_scoring_dataset`

This dataset has the following schema:

```buildoutcfg
class Submission(Record):
    name = String()
    email = String()
    ip = String()
    timestamp = Integer()
```

In your editor, you will see these methods that need to be defined:

* `pipelines`
* `feature_extraction`
* `scale`
* `label_extraction`
* `done`

Everything starts with the `pipelines` method. This is the method that gets called. It should return the pipelines that you wish to run.

```buildoutcfg
Pipelines().add(
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

The above pipeline is provided for you. It executes 7 steps, three of which are defined by you, three are defined for you through the base class. You can overwrite them if you would like.

For more information on pipelines, please read our full documentation.

Next, lets handle **label_extraction**.

Here we are going to say if the email has hotmail or yahoo in it. You can change this to be anything you would like.

This is obviously a fictitious classification, something that could be more valuable is if the lead is spam or not. This would require a labeled dataset instead of the synthetic dataset used here, which is why the classification is based on the raw data.

```buildoutcfg
def label_extraction(self, result={}):
    result['labels'] = 1 if 'yahoo' in self.input.email or 'hotmail' in self.input.email else 0
        return result
    return result
```

Next, lets look at the **feature_extraction**. This is where the fun begins.

This function can do anything you'd like, all it needs to return is the features as a dictionary.

Here we turn the text found in the dataset into numbers using the HashingVecorizer from Scikit-learn.

Then we add a feature seeing how similar the name is to the email.

Following that we turn a timestamp into a couple extra features to make it easier to see if the hour of a submission has any effect, etc.

```buildoutcfg
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
```

Next, we have one important property we need to define.

This is the `model` property. Let us try a `AdaptiveRandomForestClassifier` model.

Let us import it: `from pandioml.model import AdaptiveRandomForestClassifier`

Now, we set the model property to the model:

```buildoutcfg
class Function(FunctionBase):
    model = AdaptiveRandomForestClassifier()
```

Lastly we need to define the output. The output typically contains the prediction. Type safety is as important for the input as it is for the output that is going to be processed.

For this, you'll want to define a new class inside of the `function.py` file.

In this example, we'll use one field `Time` from the input, but add one more field for the prediction.

```buildoutcfg
class SubmissionPrediction(Record):
    name = String()
    email = String()
    ip = String()
    timestamp = Integer()
    prediction = Integer()
```

Now that the class is defined, we can add the `done` method that uses this class.

```buildoutcfg
def done(self, result={}):
    return SubmissionPrediction(name=self.input.name, email=self.input.email, ip=self.input.ip,
                                    timestamp=self.input.timestamp, prediction=result['prediction'])
```

Done! Now you can continue to test your pipeline in the next step.

## Test Your Pipeline

`pandiocli test --project_folder_name lead_scoring --dataset_name lead_scoring_dataset --loops 1000`

## Deploy Your Pipeline

`pandiocli function upload --project_folder lead_scoring`

## Deploy Your Dataset

`pandiocli dataset upload --project_folder lead_scoring_dataset`

## Full Example Code

```buildoutcfg
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

```

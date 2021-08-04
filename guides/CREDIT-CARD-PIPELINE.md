# Credit Card Pipeline

This example is found in [./examples/credit_card](./examples/credit_card) and attempts to guess if a transaction is fraud.

## Install

It is highly recommended to setup a virtual environment before installing PandioML.

This is an optional step before getting started.

`python -m venv /path/to/new/virtual/environment`

`pip install pandioml`

## Generate Project Template

`pandiocli function generate --project_name credit_card`

## Open Template File In Your Editor Of Choice

Let us create a model that attempts to predict if a credit card transaction is fraud based on the dataset `examples/credit_card_dataset`

This dataset has the following schema:

```buildoutcfg
class Transaction(Record):
    Time = Float()
    V1 = Float()
    V2 = Float()
    V3 = Float()
    V4 = Float()
    V5 = Float()
    V6 = Float()
    V7 = Float()
    V8 = Float()
    V9 = Float()
    V10 = Float()
    V11 = Float()
    V12 = Float()
    V13 = Float()
    V14 = Float()
    V15 = Float()
    V16 = Float()
    V17 = Float()
    V18 = Float()
    V19 = Float()
    V20 = Float()
    V21 = Float()
    V22 = Float()
    V23 = Float()
    V24 = Float()
    V25 = Float()
    V26 = Float()
    V27 = Float()
    V28 = Float()
    Amount = Float()
    Class = Integer()
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

Here we are going to say if it is fraud, otherwise not fraud. You can change this to be anything you would like.

```buildoutcfg
def label_extraction(self, result={}):
    result['labels'] = self.input.Class
    return result
```

Next, lets look at the **feature_extraction**. This is where the fun begins.

This function can do anything you'd like, all it needs to return is the features as a dictionary.

For this example, the data is already prepared so we just need to turn it into a dictionary and remove the label, which is the `Class` field.

```buildoutcfg
def feature_extraction(self, result={}):
    result['features'] = {k: v for k, v in self.input.__dict__.items() if 'Class' != k}

    return result
```

Next, we have one important property we need to define.

This is the `model` property. Let us try a `LogisticRegression` model.

Let us import it: `from pandioml.model import LogisticRegression`

Now, we set the model property to the model:

```buildoutcfg
class Function(FunctionBase):
    model = LogisticRegression()
```

Lastly we need to define the output. The output typically contains the prediction. Type safety is as important for the input as it is for the output that is going to be processed.

For this, you'll want to define a new class inside of the `function.py` file.

In this example, we'll use one field `Time` from the input, but add one more field for the prediction.

```buildoutcfg
class Output(Record):
    Time = Float()
    prediction = Boolean()
```

Now that the class is defined, we can add the `done` method that uses this class.

```buildoutcfg
def done(self, result={}):
    return Output(Time=self.input.Time, prediction=result['prediction'])
```

Done! Now you can continue to test your pipeline in the next step.

## Test Your Pipeline

`pandiocli test --project_folder credit_card --dataset_name credit_card_dataset --loops 1000`

## Deploy Your Pipeline

`pandiocli function upload --project_folder credit_card`

## Deploy Your Dataset

`pandiocli dataset upload --project_folder credit_card_dataset`

## Full Example Code

```buildoutcfg
from pandioml.function import FunctionBase
from pandioml.core import Pipeline, Pipelines
from pandioml.core.artifacts import artifact
from pandioml.model import LogisticRegression
from pandioml.model import StandardScaler
from pandioml.data.record import Float, Boolean, Record, Integer, JsonSchema
from pandioml.metrics import Accuracy, Precision, Recall, ConfusionMatrix


class Transaction(Record):
    Time = Float()
    V1 = Float()
    V2 = Float()
    V3 = Float()
    V4 = Float()
    V5 = Float()
    V6 = Float()
    V7 = Float()
    V8 = Float()
    V9 = Float()
    V10 = Float()
    V11 = Float()
    V12 = Float()
    V13 = Float()
    V14 = Float()
    V15 = Float()
    V16 = Float()
    V17 = Float()
    V18 = Float()
    V19 = Float()
    V20 = Float()
    V21 = Float()
    V22 = Float()
    V23 = Float()
    V24 = Float()
    V25 = Float()
    V26 = Float()
    V27 = Float()
    V28 = Float()
    Amount = Float()
    Class = Integer()
    

class Output(Record):
    Time = Float()
    prediction = Boolean()


class Function(FunctionBase):
    model = artifact.add('LogisticRegression_model', LogisticRegression())
    input_schema = JsonSchema(Transaction)
    scaler = StandardScaler()
    accuracy = Accuracy()
    precision = Precision()
    recall = Recall()
    confusion_matrix = ConfusionMatrix()

    def feature_extraction(self, result={}):
        # Remove Class from features
        result['features'] = {k: v for k, v in self.input.__dict__.items() if 'Class' != k and k[0] != '_'}

        return result

    def scale(self, result={}):
        result['features'] = self.scaler.learn_one(result['features']).transform_one(result['features'])
        return result

    def label_extraction(self, result={}):
        result['labels'] = self.input.Class

        return result

    def done(self, result={}):
        self.accuracy = artifact.add('Accuracy_Metric', self.accuracy.update(result['labels'], result['prediction']))
        self.precision = artifact.add('Precision_Metric', self.precision.update(result['labels'], result['prediction']))
        self.recall = artifact.add('Recall_Metric', self.recall.update(result['labels'], result['prediction']))
        self.confusion_matrix = artifact.add('Confusion_Matrix_Metric', self.confusion_matrix.update(result['labels'],
                                                                                                     result['prediction']))
        print(self.accuracy)
        print(self.precision)
        print(self.recall)
        print(self.confusion_matrix)
        return Output(Time=self.input.Time, prediction=result['prediction'])

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

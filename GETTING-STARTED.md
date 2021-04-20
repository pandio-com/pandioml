# Getting Started

PandioML is meant to be incredibly powerful while also being easy to use. It was built with both the beginner and the expert in mind.

## Install

It is highly recommended to setup a virtual environment before installing PandioML.

This is an optional step before getting started.

`python3 -m venv /path/to/new/virtual/environment`

`pip install pandioml pandiocli`

## Generate Project Template

`pandiocli generate test_function`

## Open Template File In Your Editor Of Choice

Let us create a model that attempts to guess the number of visitors that a restaurant will receive in a day based on the `RestaurantVisitorsDataset`

This dataset has the following schema:

```buildoutcfg
class RestaurantDay(Record):
    store_id = String()
    timestamp = Float()
    is_holiday = Boolean()
    genre_name = String()
    area_name = String()
    latitude = Double()
    longitude = Double()
    visitors = Integer()
```

In your editor, you will see four methods that need to be defined:

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

The value we are after is in the `visitors` key, so this is how we would write this function:

```buildoutcfg
def label_extraction(self, result={}):
    result['labels'] = np.array([self.input.visitors])

    return result
```

It returns a numpy array with this value extracted from the input variable, which is automatically populated with each incoming event.

Next, lets look at the **feature_extraction**. This is where the fun begins.

This function can do anything you'd like, all it needs to return is the features as a numpy array.

```buildoutcfg
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
```

Lets break this down.

The first thing we do is create a vectorizer from the `sklearn.feature_extraction.text` module. This is a great function to turn a string into numbers. The number of numbers used to represent a string is defined by `n_features`. The more the better, but remember, performance will suffer the more features you have.

Next, we're just going to use a plain Python array, so we don't have to define the numpy array shape if we were to use a numpy array. This makes it a bit easier to add and remove features a little faster.

The rest is pretty straightforward. An array is being built by the values found in `self.input`.

Next, we have three properties we need to define.

The first, is the `model` property. Let us try a `GaussianNB` model.

Let us import it: `from pandioml.model import GaussianNB`

Now, we set the model property to the model:

```buildoutcfg
class Fnc(FunctionBase):
    model = GaussianNB()
```

Next, is to define the input schema. Schema's are critically important because it enforces type safety for your pipeline. It makes sure a float is indeed a float, otherwise it will not allow the data into your pipeline.

Since we're using an existing dataset `RestaurantVisitorsDataset`, it already has a schema defined.

We will need to import two items to get the classes we need:

```buildoutcfg
from pandioml.data.record import JsonSchema, String, Float, Boolean, Double, Integer, Record
from pandioml.data import RestaurantDay
```

Now we can define our schema:

```buildoutcfg
class Fnc(FunctionBase):
    model = GaussianNB()
    input_schema = JsonSchema(RestaurantDay)
```

For more information about this dataset, you can view the following file: [RestaurantVisitorsDataset](./pandioml/data/restaurant_visitors.py)

Now, this takes care of the input schema. We also need to define the output schema. The output typically contains the prediction. Type safety is as important for the input as it is for the output that is going to be processed.

For this, you'll want to define a new class inside of the fnc.py file.

In this example, we'll use all the fields from the input, but add one more field for the prediction.

```buildoutcfg
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
```

As you can see, a single field was added to the end, that will contain our prediction.

Now that the class is defined, we can set the `output_schema`.

```buildoutcfg
class Fnc(FunctionBase):
    model = GaussianNB()
    input_schema = JsonSchema(RestaurantDay)
    output_schema = JsonSchema(RestaurantDayOutput)
```

The last thing we have to do is set the prediction field value.

Lets define a function called `done` that is executed at the completion of the pipeline.

```buildoutcfg
def done(self, result={}):
    self.output = RestaurantDayOutput(**self.input._get_fields)
    self.output.prediction = result['prediction']
    return result
```

First thing we'll do is set the output from the input. Then we'll set the prediction.

Done! Now you can continue to test your pipeline in the next step.

For a view of the complete example, go here: [Restaurant Vists fnc.py Example](./examples/restaurant_visits/fnc.py)

## Test Your Pipeline

`pandiocli test --project_folder_name test_function --dataset_name FormSubmissionGenerator --loops 1000`

## Deploy Your Pipeline

`pandiocli function upload --project_folder test_function`

# Quick Start

## Create a model in less than 1 minute!

1. `cd pandioml && ./build.sh && cd ../`

1. `cd pandiocli && ./build.sh && cd ../`

1. `pandiocli register your@gmail.com`

1. `python examples/form_fraud/runner.py --dataset_name FormSubmissionGenerator --loops 500`

A graph showing the model accuracy will be generated after running the example.

## Create a custom model in less than 10 minutes!

1. `cd pandioml && ./build.sh && cd ../`

1. `cd pandiocli && ./build.sh && cd ../`

1. `pandiocli register your@gmail.com`

1. `pandiocli generate test_function`

1. `cd test_function`

1. Open `fnc.py` in your favorite editor, put your pipelines code in the `pipelines` method.

1. `python runner.py --dataset_name FormSubmissionGenerator --loops 500`

      FormSubmissionGenerator is used in this example, but any dataset or generator from `pandioml.data.*` can be used. Or you can build your own as described below.

A graph showing the model accuracy will be generated after running the example.

*Tip: Open up an example `fnc.py` to get a jumpstart inside one of the examples in the `./examples` directory*

# Important Concepts

### Datasets & Generators

Many datasets and generators are included with PandioML. Your own data can be used easily by creating your own Dataset or Generator.

### Algorithms

Dozens of the most popular algorithms are available to easily use in your pipelines.

#### Evaluators

Dozens of evaluators are included to help calculate performance metrics for models.

#### Metrics

Save time by using common methods to calculate metrics from your data.

### Pipelines

Based off of scikit-learn, use new and improved pipelines to increase productivity and efficiency.
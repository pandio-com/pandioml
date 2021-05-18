# Getting Started

PandioML is meant to be incredibly powerful while also being easy to use. It was built with both the beginner and the expert in mind.

## Install

It is highly recommended to setup a virtual environment before installing PandioML.

This is an optional step before getting started.

`python3 -m venv /path/to/new/virtual/environment`

`pip install pandioml`

## Generate Project Template

`pandiocli function generate --project_name test_function`

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
    result['labels'] = self.input.visitors

    return result
```

It sets `labels` to an integer value extracted from the input variable, which is automatically populated with each incoming event.

Next, lets look at the **feature_extraction**. This is where the fun begins.

This function can do anything you'd like, all it needs to return is the features as a dictionary.

```buildoutcfg
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

Now that the class is defined, we can add the `output` method that uses this class.

```buildoutcfg
def done(self, result={}):
    output = RestaurantDayOutput(**dict((lambda x: (x, getattr(self.input, x)))(key) for key in
                                             self.input._fields.keys()))

    output.prediction = result['prediction']

    return output
```

Done! Now you can continue to test your pipeline in the next step.

For a view of the complete example, go here: [Restaurant Vists function.py Example](./examples/restaurant_visits/function.py)

## Test Your Pipeline

`pandiocli test --project_folder test_function --dataset_name RestaurantVisitorsDataset --loops 1000`

## Deploy Your Pipeline

`pandiocli function upload --project_folder test_function`

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
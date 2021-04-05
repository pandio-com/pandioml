<a href="https://pandio.com"><img src="assets/pandio_225_blue-05.svg" alt="Pandio Logo"></a>

Learn more about Pandio at https://pandio.com

# Pandio Machine Learning

This repository contains the PandioML library and CLI tool to develop machine learning on the Pandio platform.

## Getting Started

### Create a model in less than 1 minute!

1. `python pandioml/setup.py install`

1. `cd pandiocli && python setup.py install && cd ../`

1. `pandiocli register your@gmail.com`

1. `python examples/form_fraud/runner.py --dataset_name FormSubmissionGenerator --loops 500`

A graph showing the accuracy will be shown and the model will be saved as `example.model`

## Create a custom model in less than 10 minutes!

1. `python pandioml/setup.py install`

1. `cd pandiocli && python setup.py install && cd ../`

1. `pandiocli register your@gmail.com`

1. `pandiocli generate test_function`

1. `cd test_function`

1. Open `function.py` in your favorite editor, put your pipelines code in the `pipelines` method.

1. `python runner.py --dataset_name FormSubmissionGenerator --loops 500`

A graph showing the accuracy will be shown and the model will be saved as `example.model`

## PandioML

### Installation

`pip install pandioml`

### Documentation

#### Model

The `pandioml.model.*` module handles all of the available algorithms and models.

| Module | Description
| ---|---|
| pandioml.model.NaiveBayes | Performs classic bayesian prediction while making naive assumption that all inputs are independent.
| pandioml.model.HoeffdingTreeClassifier | Hoeffding Tree or Very Fast Decision Tree classifier.
| pandioml.model.HoeffdingAdaptiveTreeClassifier | Hoeffding Adaptive Tree classifier.

#### Data

The `pandioml.data.*` model contains all of the datasets and generators available.

| Module | Description | Schema | Labeled |
| ---|---|---|---|
| pandioml.data.FormSubmissionGenerator | Uses the Faker Python package to generate an infinite amount of form submissions. | [schema](./pandioml/data/form_submissions.py#L35) | No
| pandioml.data.WebHostingDataset | Contains 4,500,000 server resource metrics recorded over a 3 month period of time. | [schema](./pandioml/data/hosting.py#L86) | No
| pandioml.data.PersonProfile | Generates an infinite stream of user Profiles using the Faker Python library. | [schema](./pandioml/data/people.py#L38) | No

##### Create Your Own Dataset or Generator

Use the `pandioml.data.Stream` class, inherit it, define the required methods, and use your own data inside of PandioML!

To make it available on Pandio's platform, `pandiocli upload` it using the PandioCLI, then `pandiocli deploy` it.

#### Build Streaming Pipelines

The `pandioml.core.pipelines` contains a pipeline framework to build traditional machine learning pipelines.

The PandioML framework for building pipelines is similar to `scikit-learn`'s, but differs in that the pipeline is meant to process a single record, instead of a batch of records.

Two classes make up this framework. More information on each class follows:

##### Pipelines

This class was built as a container for pipelines, holding an internal list of individual pipelines with name references to each pipeline.

Its job is to provide an iterable list of pipelines to execute asynchronously.

Commonly, pipelines will be added manually with the `add` method.

For large pipelines, such as hypertuning thousands of parameters, the `build` method can be overwritten to allow the programmatic creation of large number of pipelines.

##### Pipeline

The pipeline class follows the traditional purpose of building a pipeline, but it uses a different syntax taken from Promise libraries in JavaScript.

Instead of passing a list of steps, each step is declared using the `then` method. Additional methods like `final`, `done`, and `catch` are provided to make the pipeline easier to reason about.

`final` always the last step to run, regardless of where it is defined.

`done` runs when all steps are complete. This is commonly used to control what is returned from the pipeline.

`catch` allows any exception to be handled in a single place.

Here are a few examples of how the methods work:

**How To Pass Variables**
```buildoutcfg
def label_extraction(classification):
    print(f"Classification variable is: {classification}")

Pipeline(*args, **kwargs)
    .then(label_extraction, 'categories')
```

##### Important Note

All implementations in PandioML will always be an instance of Pipelines, even if only one Pipeline is being used. This allows Pandio's platform to perform optimizations.

##### Example Pipeline

The following code sample was pulled from `./examples/form_fraud/function.py`

```buildoutcfg
Pipelines().add(
    'inference',
    Pipeline(*args, **kwargs)
        .then(self.label_extraction)
        .then(self.feature_extraction)
        .then(self.fit)
        .final(self.predict)
        .done(self.output)
        .catch(self.error)
).add(
    'drift',
    Pipeline(*args, **kwargs)
        .then(self.detect_drift)
        .done(self.output)
        .catch(self.error)
).add(
    'evaluate',
    Pipeline(*args, **kwargs)
        .then(self.evaluate)
        .done(self.output)
        .catch(self.error)
).add(
    'inference_tree',
    Pipeline(*args, **kwargs)
        .then(self.set_model, HoeffdingTreeClassifier)
        .then(self.label_extraction)
        .then(self.feature_extraction)
        .then(self.fit)
        .final(self.predict)
        .done(self.output)
        .catch(self.error)
)
```

This pipeline works similar to [scikit-learn](https://scikit-learn.org/stable/)'s pipeline, but improves upon it by making it easier to follow and includes helper methods.

If you have your own pipeline library or existing pipeline code, that may be used as well.

#### Examples

##### `./examples/form_fraud`

This example combines a NaiveBayes model, with the FormSubmissionGenerator, and a pipeline to demonstrate how to predict whether an email is from Yahoo.com or Hotmail.com

This demonstrates an end to end example of how PandioML accelerates the process of building, deploying, and orchestrating models.

#### Function

This is the core of PandioML. All of the helper methods, magic sauce, embedded packages, cli tools, etc. exist to help build functions that run on the Pandio platform. In each of these functions is typically a model that makes accurate predictions. What data it uses, the algorithm, feature extractions, fitting, predicting, pipelining, and even labeling, is completely up to you. The function is your sandbox, where all the fun begins. Everything in PandioML is meant to help make creating value with machine learning easier.

Only two things are required to be defined in the function file generated for each project, the `model` you'd like to use, and the `pipelines` you'd like to execute against each individually streamed event.

Any number of classes or methods may be created to assist in the building of the function.

The `pandioml.function.FunctionBase` is the core component to building a model with PandioML. It provides helper methods and abstract methods that make it easy to build and deploy models.

The `pandioml.function.Context` provides local helper methods to simulate what is available when deployed to production to allow faster local iterative testing.

The `pandioml.function.Storage` provides access to a distributed key value storage service that is eventually consistent.

The `pandioml.function.Logger` provides local helper methods to simulate what is available when deployed to production to allow faster local iterative testing.

The `Fnc` class defined inside of the functions file has three important variables defined for you:

1. `Fnc.id`

      This is the `id` of the function instance. A unique `id` for the individual instance of the function. If 4 instances of the function were running, this would be 4 unique values, one for each instance of the function running.
      
1. `Fnc.input`

      This is an individual event record whose type depends on the data placed on the input topic, or the data object selected when testing locally.

1. `Fnc.storage`

      This is a class that provides access to the distributed storage that is eventually consistent and accessible to all functions. This is a great place to store data about a function as it runs, as well as communicate to other functions running.

## PandioCLI

### Installation

`pip install pandiocli`

### Commands

#### `pandiocli generate folder_name`

Generates a project template in the current working directory at `./folder_name`

1. `./folder_name/runner.py`

      This is a helper function that allows you to use Python locally to test the function end to end.
      
1. `./folder_name/function.py`

      This is the file where all of your logic should be placed.

1. `./folder_name/wrapper.py`

      This function is called by the `runner.py`, which then subsequently imports your custom code. This is the file that gets deployed to Pandio's platform. Ideally this file does not get modified.

1. `./folder_name/requirements.txt`

      This file should contain all the necessary Python packages to power `function.py`. The contents of this will automatically be installed for you when deploying to Pandio's platform. When running locally, make sure to install as you normally would `pip install -r requirements.txt`

#### `pandiocli config show`

This will output the current configuration for the PandioCLI

#### `pandiocli config set --key PANDIO_TOKEN --value ABC123`

This command allows you to manually set the configuration parameters for PandioCLI

* PANDIO_CONNECTION_STRING
* PANDIO_TENANT
* PANDIO_SECRET_KEY
* PANDIO_EMAIL

#### `pandiocli test --project_folder_name folder_name --dataset_name FormSubmissionGenerator --loops 1000`

This is a helper method to running the `folder_name/runner.py` file manually with Python.

**project_folder_name** is the relative path to the project folder.

**dataset_name** is the name of the `pandioml.data` datasets and generators available inside of PandioML.

**loops** is the number of events to process. Most streams of data are infinite, so this allows iterative testing with limited data.

#### `pandiocli performance --project_folder_name folder_name --dataset_name FormSubmissionGenerator --loops 1000`

This is similar to the `test` method above, but it will run some performance checks looking for excessive CPU usage, memory leaks, and more.

**project_folder_name** is the relative path to the project folder.

**dataset_name** is the name of the `pandioml.data` datasets and generators available inside of PandioML.

**loops** is the number of events to process. Most streams of data are infinite, so this allows iterative testing with limited data.

#### `pandiocli function upload --project_folder folder_name`

Package up your project and upload it to Pandio's platform.

#### `pandiocli register your@email.com`

This command registers a Pandio.com account for you. An email with a link to verify your registration will be sent.

Once the link is clicked, the local PandioCLI will be configured successfully with your new Pandio account.

If you already have a Pandio.com account, you'll need to use the `pandiocli config` command to manually set the configuration with values inside of the Pandio.com Dashboard.

# TODO

Figure out how to bubble up the exception from the function/pipeline. function/base.py error method

Track down memory leak: https://www.fugue.co/blog/diagnosing-and-fixing-memory-leaks-in-python.html

Add `pandiocli performance --project_folder_name examples/form_fraud --dataset_name FormSubmissionGenerator --loops 1000` that will automatically profile the function and output recommendations. Check speed, memory, etc as it runs.

Maybe integrate this simulator? https://github.com/namebrandon/Sparkov_Data_Generation

Allow `Pipelines` to be built programmatically at runtime, to allow the potential for thousands to be built easily.

# Potential Datasets

./scripts/credit-card-fraud.arff - https://weka.8497.n7.nabble.com/file/n23121/credit_fruad.arff

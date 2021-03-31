<a href="https://pandio.com"><img src="assets/pandio_225_blue-05.svg" alt="Pandio Logo"></a>

Learn more about Pandio at https://pandio.com

# Pandio Machine Learning

This repository contains the PandioML library and CLI tool to develop machine learning on the Pandio platform.

## PandioML

### Installation

`pip install pandioml`

### Documentation

#### Model

The `pandioml.model.*` module handles all of the available algorithms and models.

| Module | Description |
| ---|---|
| pandioml.model.NaiveBayes | Performs classic bayesian prediction while making naive assumption that all inputs are independent. |
| pandioml.model.HoeffdingTreeClassifier | Hoeffding Tree or Very Fast Decision Tree classifier. |
| pandioml.model.HoeffdingAdaptiveTreeClassifier | Hoeffding Adaptive Tree classifier. |

#### Data

The `pandioml.data.*` model contains all of the datasets and generators available.

| Module | Description |
| ---|---|
| pandioml.data.FormSubmissionGenerator | Uses the Faker Python package to generate an infinite amount of form submissions. |
| pandioml.data.WebHostingDataset | Contains 4,500,000 server resource metrics recorded over a 3 month period of time. |

##### Create Your Own Dataset or Generator

Use the `pandioml.data.Stream` class, inherit it, define the required methods, and use your own data inside of PandioML!

To make it available on Pandio's platform, `pandiocli upload` it using the PandioCLI, then `pandiocli deploy` it.

#### Pipeline

The `pandioml.core.pipeline` contains a pipeline framework to build traditional machine learning pipelines.

The following code sample was pulled from `./examples/form_fraud/function.py`

```buildoutcfg
Pipeline(*args, **kwargs) \
    .then(self.label_extraction, input=kwargs['input']) \
    .then(self.feature_extraction, input=kwargs['input']) \
    .then(self.fit) \
    .final(self.predict) \
    .done(self.output) \
    .catch(self.error)
```

This pipeline works similar to [scikit-learn](https://scikit-learn.org/stable/)'s pipeline, but improves upon it by making it easier to follow and includes helper methods.

If you have your own pipeline library or existing pipeline code, that may be used as well.

#### Examples

##### `./examples/form_fraud`

This example combines a NaiveBayes model, with the FormSubmissionGenerator, and a pipeline to demonstrate how to predict whether an email is from Yahoo.com or Hotmail.com

This demonstrates an end to end example of how PandioML accelerates the process of building, deploying, and orchestrating models.

#### Function

The `pandioml.function.FunctionBase` is the core component to building a model with PandioML. It provides helper methods and abstract methods that make it easy to build and deploy models.

The `pandioml.function.Context` provides local helper methods to simulate what is available when deployed to production to allow faster local iterative testing.

The `pandioml.function.Logger` provides local helper methods to simulate what is available when deployed to production to allow faster local iterative testing.

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

## Getting Started

### Create a model in less than 1 minute!

1. `python pandioml/setup.py install`

1. `cd pandiocli && python setup.py install && cd ../`

1. `pandiocli register your@gmail.com`

1. `python examples/form_fraud/runner.py`

A graph showing the accuracy will be shown and the model will be saved as `example.model`

## Create a custom model in less than 10 minutes!

1. `python pandioml/setup.py install`

1. `cd pandiocli && python setup.py install && cd ../`

1. `pandiocli register your@gmail.com`

1. `pandiocli generate test_function`

1. `cd test_function`

1. Open `function.py` in your favorite editor, put your pipeline code in the `pipeline` method.

1. `python runner.py --project_name ./ --dataset_name FormSubmissionGenerator --loops 1000`

A graph showing the accuracy will be shown and the model will be saved as `test.model`

# TODO

Figure out how to bubble up the exception from the function/pipeline. function/base.py error method

Track down memory leak: https://www.fugue.co/blog/diagnosing-and-fixing-memory-leaks-in-python.html

Add `pandiocli performance --project_folder_name examples/form_fraud --dataset_name FormSubmissionGenerator --loops 1000` that will automatically profile the function and output recommendations. Check speed, memory, etc as it runs.
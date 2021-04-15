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

Add your pipelines code to `./test_function/fnc.py`

The following example was taken from `./examples/form_fraud/fnc.py`

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
)
```

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
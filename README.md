<a href="https://pandio.com"><img src="assets/pandio_225_blue-05.svg" alt="Pandio Logo"></a>

Learn more about Pandio at https://pandio.com

# PandioML - Pandio.com Machine Learning

This repository contains the PandioML Python library and PandioCLI tool to develop and deploy machine learning for streaming data.

*PandioML is currently in private alpha testing, please email ml@pandio.com for access.*

## About PandioML

**Incremental Learning**

As data is streamed in, stream learning models are created incrementally and updated continously. They are extremely powerful in a real-time environment, but can also be a viable replacement for traditional machine learning.

**Adaptive Learning**

Data distribution changes have far less impact from concept drift on a stream learning model due to the adaptive nature of incremental learning.

**Resource Efficient**

Due to the incremental learning, considerably less processing time and memory are needed to train a model.

**Easy To Use**

PandioML is based on scikit-learn, making it easy to pickup.

**Open Source**

Based on powerful open source technology itself, PandioML is released under MIT License.

**AI Orchestration**

Not just a Python library, PandioCLI makes it easy to package and deploy PandioML pipelines and models to the Pandio platform.

## Use Cases

**Supervised Learning**

When working with labeled data. Depending on the target type can be either classification (discrete values) or regression (continuous values)

**Single & Multiple Output**

Single-output methods predict a single target-label (binary or multi-class) for classification or a single target-value for regression. Multi-output methods simultaneously predict multiple variables given an input.

**Concept Drift Detection**

Changes in data distribution can harm learning. Drift detection methods are designed to rise an alarm in the presence of drift and are used alongside learning methods to improve their robustness against this phenomenon in evolving data streams.

**Unsupervised Learning**

When working with unlabeled data. For example, anomaly detection where the goal is the identification of rare events or samples which differ significantly from the majority of the data.

**Building Pipelines**

Scikit-learn pipelines on steroids! Familiar syntax with more helper methods to make building and debugging pipelines easier.

**Deploying Models**

After writing (or re-using) your pipeline and model, deploy to Pandio's AI Orchestration platform with a single command. Your model is now available for production use at any scale!

## About Pandio.com

Pandio is an AI Orchestration platform that helps companies accelerate their AI initiatives. Connect data, build pipelines, train models, and deploy models on your terms at unmatched speed and scale.

## Requirements

This library requires Python version 3.5 through 3.8 to support all functionality.

## How It Works

<img src="assets/PandioML+PandioCLI.svg" alt="Architecture Diagram">

#### Read Our [Getting Started](./GETTING-STARTED.md) Guide

## PandioML

### Installation

`pip install pandioml`

### Documentation

#### Model

The `pandioml.model.*` module handles all of the available algorithms and models.

| Module | Description
| ---|---|
| GaussianNB | Gaussian Naive Bayes
| MultinomialNB | Naive Bayes classifier for multinomial models.
| ComplementNB | Naive Bayes classifier for multinomial models.
| BernoulliNB | Bernoulli Naive Bayes.
| K-means | Incremental k-means.
| ADWINBaggingClassifier | ADWIN Bagging classifier.
| BaggingClassifier | Online bootstrap aggregation for classification.
| BaggingRegressor | Online bootstrap aggregation for regression.
| AdaBoostClassifier | Boosting for classification
| SRPClassifier | Streaming Random Patches ensemble classifier.
| EpsilonGreedyRegressor | Epsilon-greedy bandit algorithm for regression.
| UCBRegressor | Upper Confidence Bound bandit for regression.
| EWARegressor | Exponentially Weighted Average regressor.
| SuccessiveHalvingClassifier | Successive halving algorithm for classification.
| SuccessiveHalvingRegressor | Successive halving algorithm for regression.
| StackingClassifier | Stacking for binary classification.
| FFMClassifier | Field-aware Factorization Machine for binary classification.
| FFMRegressor | Field-aware Factorization Machine for regression.
| FMClassifier | Factorization Machine for binary classification.
| FMRegressor | Factorization Machine for regression.
| FwFMClassifier | Field-weighted Factorization Machine for binary classification.
| FwFMRegressor | Field-weighted Factorization Machine for regression.
| HOFMClassifier | Higher-Order Factorization Machine for binary classification.
| HOFMRegressor | Higher-Order Factorization Machine for regression.
| HardSamplingClassifier | Hard sampling classifier.
| HardSamplingRegressor | Hard sampling regressor.
| RandomOverSampler | Random over-sampling.
| RandomSampler | Random sampling by mixing under-sampling and over-sampling.
| RandomUnderSampler | Random under-sampling.
| HoeffdingTreeClassifier | Hoeffding Tree or Very Fast Decision Tree classifier.
| HoeffdingAdaptiveTreeClassifier | Hoeffding Adaptive Tree classifier.
| ExtremelyFastDecisionTreeClassifier | Extremely Fast Decision Tree classifier.
| LabelCombinationHoeffdingTreeClassifier | Label Combination Hoeffding Tree for multi-label classification.
| HoeffdingTreeRegressor | Hoeffding Tree regressor.
| HoeffdingAdaptiveTreeRegressor | Hoeffding Adaptive Tree regressor.
| iSOUPTreeRegressor | Incremental Structured Output Prediction Tree (iSOUP-Tree) for multi-target regression.
| StackedSingleTargetHoeffdingTreeRegressor | Stacked Single-target Hoeffding Tree regressor.
| KNNClassifier | k-Nearest Neighbors classifier.
| KNNADWINClassifier | K-Nearest Neighbors classifier with ADWIN change detector.
| SAMKNNClassifier | Self Adjusting Memory coupled with the kNN classifier.
| KNNRegressor | k-Nearest Neighbors regressor.
| AccuracyWeightedEnsembleClassifier | Accuracy Weighted Ensemble classifier
| AdaptiveRandomForestClassifier | Adaptive Random Forest classifier.
| AdaptiveRandomForestRegressor | Adaptive Random Forest regressor.
| AdditiveExpertEnsembleClassifier | Additive Expert ensemble classifier.
| BatchIncrementalClassifier | Batch Incremental ensemble classifier.
| ClassifierChain | Classifier Chains for multi-label learning.
| ProbabilisticClassifierChain | Probabilistic Classifier Chains for multi-label learning.
| MonteCarloClassifierChain | Monte Carlo Sampling Classifier Chains for multi-label learning.
| DynamicWeightedMajorityClassifier | Dynamic Weighted Majority ensemble classifier.
| LearnPPNSEClassifier | Learn++.NSE ensemble classifier.
| LearnPPClassifier | Learn++ ensemble classifier.
| LeveragingBaggingClassifier | Leveraging Bagging ensemble classifier.
| MultiOutputLearner | Multi-Output Learner for multi-target classification or regression.
| OnlineAdaC2Classifier | Online AdaC2 ensemble classifier.
| OnlineBoostingClassifier | Online Boosting ensemble classifier.
| OnlineCSB2Classifier | Online CSB2 ensemble classifier.
| OnlineRUSBoostClassifier | Online RUSBoost ensemble classifier.
| OnlineSMOTEBaggingClassifier | Online SMOTEBagging ensemble classifier.
| OnlineUnderOverBaggingClassifier | Online Under-Over-Bagging ensemble classifier.
| OzaBaggingClassifier | Oza Bagging ensemble classifier.
| OzaBaggingADWINClassifier | Oza Bagging ensemble classifier with ADWIN change detector.
| RegressorChain | Regressor Chains for multi-output learning.
| StreamingRandomPatchesClassifier | Streaming Random Patches ensemble classifier.
| ADWIN | Adaptive Windowing method for concept drift detection.
| DDM | Drift Detection Method.
| EDDM | Early Drift Detection Method.
| HDDM_A | Drift Detection Method based on Hoeffding’s bounds with moving average-test.
| HDDM_W | Drift Detection Method based on Hoeffding’s bounds with moving weighted average-test.
| KSWIN | Kolmogorov-Smirnov Windowing method for concept drift detection.
| PageHinkley | Page-Hinkley method for concept drift detection.
| EvaluateHoldout | The holdout evaluation method or periodic holdout evaluation method.
| EvaluatePrequential | The prequential evaluation method or interleaved test-then-train method.
| EvaluatePrequentialDelayed | The prequential evaluation delayed method.
| VeryFastDecisionRulesClassifier | Very Fast Decision Rules classifier.
| RobustSoftLearningVectorQuantization | Robust Soft Learning Vector Quantization for Streaming and Non-Streaming Data.
| HalfSpaceTrees | Implementation of the Streaming Half–Space–Trees (HS–Trees)

#### Data

The `pandioml.data.*` model contains all of the datasets and generators available.

| Module | Description | Schema | Labeled |
| ---|---|---|---|
| FormSubmissionGenerator | Uses the Faker Python package to generate an infinite amount of form submissions. | [schema](./pandioml/pandioml/data/form_submissions.py#L28-L31) | No
| WebHostingDataset | Contains 12,496,728 server resource metric events recorded over a 3 month period of time. | [schema](./pandioml/pandioml/data/hosting.py#L64-L82) | No
| PersonProfile | Generates an infinite stream of user Profiles using the Faker Python library. | [schema](./pandioml/pandioml/data/people.py#L31-L34) | No
| CreditCardFraud | A dataset of 1,296,675 credit card transactions with a percentage labeled as fraud. | [schema](./pandioml/pandioml/data/credit_card_transactions.py#L72-L99) | Yes
| AgrawalGenerator | A generator for data regarding home loan applications with the ability to balance and add noise. | [schema](./pandioml/pandioml/data/agrawal.py#L45-L55) | Yes
| PhishingDataset | 1250 entries of webpages that are classified as phishing or not. | [schema](./pandioml/pandioml/data/phishing_dataset.py#L36-L46) | Yes
| MovieRatingDataset | 100,000 movie ratings from different types of individuals. | [schema](./pandioml/pandioml/data/movie_ratings.py#L37-L48) | Yes
| RestaurantVisitorsDataset | This dataset contains 252,108 records over a 16 week period to 829 Japanese Restaurants. | [schema](./pandioml/pandioml/data/restaurant_visitors.py#L37-L45) | Yes

#### Metrics

The `pandioml.metrics.*` contains helper methods to calculate metrics relating to the pipelines.

| Module | Description
| ---|---|
| Accuracy | Accuracy score, which is the percentage of exact matches.
| BalancedAccuracy | Balanced accuracy.
| BinaryMetric | Mother class for all binary classification metrics.
| ClassificationMetric | Mother class for all classification metrics.
| ClassificationReport | A report for monitoring a classifier.
| CohenKappa | Cohen's Kappa score.
| CrossEntropy | Multiclass generalization of the logarithmic loss.
| ExactMatch | Exact match score.
| ExamplePrecision | Example-based precision score for multilabel classification.
| ExampleRecall | Example-based recall score for multilabel classification.
| ExampleF1 | Example-based F1 score for multilabel classification.
| ExampleFBeta | Example-based F-Beta score.
| F1 | Binary F1 score.
| FBeta | Binary F-Beta score.
| GeometricMean | Geometric mean score.
| Hamming | Hamming score.
| HammingLoss | Hamming loss score.
| Jaccard | Jaccard index for binary multi-outputs.
| KappaM | Kappa-M score.
| KappaT | Kappa-T score.
| LogLoss | Binary logarithmic loss.
| MAE | Mean absolute error.
| MacroF1 | Macro-average F1 score.
| MacroFBeta | Macro-average F-Beta score.
| MacroPrecision | Macro-average precision score.
| MacroRecall | Macro-average recall score.
| MCC | Matthews correlation coefficient.
| Metric | Mother class for all metrics.
| Metrics | A container class for handling multiple metrics at once.
| MicroF1 | Micro-average F1 score.
| MicroFBeta | Micro-average F-Beta score.
| MicroPrecision | Micro-average precision score.
| MicroRecall | Micro-average recall score.
| MultiClassMetric | Mother class for all multi-class classification metrics.
| MultiFBeta | Multi-class F-Beta score with different betas per class.
| MultiOutputClassificationMetric | Mother class for all multi-output classification metrics.
| MultiOutputRegressionMetric | Mother class for all multi-output regression metrics.
| MSE | Mean squared error.
| Precision | Binary precision score.
| Recall | Binary recall score.
| RegressionMetric | Mother class for all regression metrics.
| RegressionMultiOutput | Wrapper for multi-output regression.
| RMSE | Root mean squared error.
| RMSLE | Root mean squared logarithmic error.
| ROCAUC | Receiving Operating Characteristic Area Under the Curve.
| Rolling | Wrapper for computing metrics over a window.
| R2 | Coefficient of determination ($R^2$) score
| SMAPE | Symmetric mean absolute percentage error.
| TimeRolling | Wrapper for computing metrics over a period of time.
| WeightedF1 | Weighted-average F1 score.
| WeightedFBeta | Weighted-average F-Beta score.
| WeightedPrecision | Weighted-average precision score.
| WeightedRecall | Weighted-average recall score.
| WrapperMetric | Metric Wrapper
| BallHall | Ball-Hall index
| BIC | Bayesian Information Criterion (BIC).
| CalinskiHarabasz | Calinski-Harabasz index (CH).
| Cohesion | Mean distance from the points to their assigned cluster centroids. The smaller the better.
| DaviesBouldin | Davies-Bouldin index (DB).
| GD43 | Generalized Dunn's index 43 (GD43).
| GD53 | Generalized Dunn's index 53 (GD53).
| Hartigan | Hartigan Index (H - Index)
| IIndex | I-Index (I).
| InternalMetric | Mother class of all internal clustering metrics.
| MSSTD | Mean Squared Standard Deviation.
| PS | Partition Separation (PS).
| CR2 | R-Squared
| RMSSTD | Root Mean Squared Standard Deviation.
| SD | The SD validity index (SD).
| Separation | Average distance from a point to the points assigned to other clusters.
| Silhouette | Silhouette coefficient [^1], roughly speaking, is the ratio between cohesion and the average distances from the points to their second-closest centroid.
| SSB | Sum-of-Squares Between Clusters (SSB).
| SSW | Sum-of-Squares Within Clusters (SSW).
| XieBeni | Xie-Beni index (XB).
| WB | WB Index
| Xu  | Xu Index

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

For large pipelines, such as hypertuning thousands of parameters, a loop could be written to allow the programmatic creation of large number of pipelines.

```buildoutcfg
class Fnc(FunctionBase):
    def pipelines(self):
        pp = Pipelines()
        for i in range(0, 1000):
            pp.add(
                f"inference_{i}",
                Pipeline(*args, **kwargs)
                    .then(self.set_model_parameter, i)
                    .then(self.label_extraction)
                    .then(self.feature_extraction)
                    .then(self.fit)
                    .final(self.predict)
                    .done(self.output)
                    .catch(self.error)
            )
        return pp

```

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

The following code sample was pulled from `./examples/form_fraud/fnc.py`

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

#### Artifacts

Reproducible pipelines are a critically important part of data science.

PandioML provides a tool to store any artifact associated with a pipeline.

3 artifacts are automatically stored for you:

1. Dataset

1. Pipeline

1. Model

If you'd like to store additional things, such as metrics, charts, hypertuning parameters, or anything else, it can be done by importing the artifact module like so:

`from pandioml.core.artifacts import artifact`

Then, call the `add` method of the `artifact` as follows:

`dict = artifact.add('config_params', {'foo': 'bar'})`

The first parameter is a unique name for it, the second is the item to be stored. If it can be pickled, it can be stored as an artifact. In addition, there are times when it is preferred to defer the artifact, so a callable is also acceptable as the item to be stored. When called, a single argument is passed called `storage_location` that contains where the artifacts will be stored. This makes it easy to provide custom logic when storing artifacts.

Bonus, the method will return the artifact, so that you can easily add items and define things in a single line.

Additionally, a `save` method exists that can be manually called to store artifacts. The storage medium used to store these artifacts can also be extended. Currently, File and AWS S3 storage backends are supported. The default storage backend is File.

This method is called automatically when the function stops running. You may call it yourself, but not too often as it is an expensive operation depending on the size of the artifacts.

`ARTIFACT_STORAGE` inside of `config.py` defines where the artifacts are stored. This can be overwritten through the call to `save` as well.

#### Schema Registry Support

Type safety is critically important to any data science initiative. If you can't rely on a float being a float, that can have dangerous consequences.

PandioML treats type safety as a first class citizen. Before data is streamed into your pipeline, you can require that it validates against a defined schema. If it fails validation, your pipeline will never see it.

Type safety in PandioML prevents potential disastrous situations and makes pipeline development more efficient and productive.

To give an example, the following class defines a schema that the data must follow. Additionally, the data comes in as an object built right from the schema.

```buildoutcfg
class Transaction(Record):
    trans_date_trans_time = String()
    cc_num = Integer()
    merchant = String()
    category = String()
    amt = Float()
    first = String()
    last = String()
    gender = String()
    street = String()
    city = String()
    state = String()
    zip = Integer()
    lat = Float()
    long = Float()
    city_pop = Integer()
    job = String()
    dob = String()
    trans_num = String()
    unix_time = Integer()
    merch_lat = Float()
    merch_long = Float()
    is_fraud = Integer()
    weekday = Integer()
    weekend = Integer()
    month = Integer()
    day = Integer()
    hour = Integer()
```

Using the above as an example, as data is streamed into your pipeline, it comes in as a Transaction object.

This allows you to quickly access properties like so: `event.cc_num`

Data science is so much easier with type safety offered by schemas!

#### Debugging With PandioML Interactive Sessions

Have you ever asked yourself one of these questions?

* What in the heck happened?
* What does that error mean?
* That value is not right... what part of my code did that?
* My pipeline does not work, what is the problem?

If you have, you're not alone. If you haven't, feel free to skip this section!

To help find the problem and fix it quickly, PandioML has the ability to start an interactive session from any point in your code. This will halt execution and open up an interactive Python session that lets you inject code into your code execution in real time. No need to add a bunch of print statements to figure out what is happening!

To start an interactive session, import the interactive method from here:

`from pandioml.core import interact`

Then call it like so: `interact(banner='Helpful Note Where This Was Triggered', local=locals())`

When you run your code, it will halt where this method is called, letting you inject any Python code you would like into the execution.

With `local`, you can change scope of the variables, and access `local=globals()` if you'd like.

You can also add many of these calls all throughout your code. When you're ready to continue the execution of your code, simply type `CTRL + D`.

Happy debugging!

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
      
1. `./folder_name/fnc.py`

      This is the file where all of your logic should be placed.

1. `./folder_name/wrapper.py`

      This function is called by the `runner.py`, which then subsequently imports your custom code. This is the file that gets deployed to Pandio's platform. Ideally this file does not get modified.

1. `./folder_name/requirements.txt`

      This file should contain all the necessary Python packages to power `fnc.py`. The contents of this will automatically be installed for you when deploying to Pandio's platform. When running locally, make sure to install as you normally would `pip install -r requirements.txt`

1. `./folder_name/config.py`

      This contains non-sensitive configuration parameters for the project. Sensitive configuration parameters are set via the PandioCLI.

#### `pandiocli config show`

This will output the current configuration for the PandioCLI

#### `pandiocli config set --key PANDIO_TOKEN --value ABC123`

This command allows you to manually set the configuration parameters for PandioCLI

* PANDIO_SECRET_KEY
* PANDIO_EMAIL

#### `pandiocli test --project_folder_name folder_name --dataset_name FormSubmissionGenerator --loops 1000`

This is a helper method to running the `folder_name/runner.py` file manually with Python. It includes performance metrics which is helpful to debug excessive resource usage such as memory leaks.

**project_folder_name** is the relative path to the project folder.

**dataset_name** is the name of the `pandioml.data` datasets and generators available inside of PandioML.

**loops** is the number of events to process. Most streams of data are infinite, so this allows iterative testing with limited data.

#### `pandiocli function upload --project_folder folder_name`

Package up your project and upload it to Pandio's platform.

#### `pandiocli register your@email.com`

This command registers a Pandio.com account for you. An email with a link to verify your registration will be sent.

Once the link is clicked, the local PandioCLI will be configured successfully with your new Pandio account.

If you already have a Pandio.com account, you'll need to use the `pandiocli config` command to manually set the configuration with values inside of the Pandio.com Dashboard.

## Contributing

All contributions are welcome.

The best ways to get involved are as follows:

1. [Issues](./issues)

    This is a great place to report any problems found with PandioML. Bugs, inconsistencies, missing documentation, or anything that acted as an obstacle to using PandioML.
    
1. [Discussions](./discussions)

    This is a great place for anything related to PandioML. Propose features, ask questions, highlight use cases, or anything else you can imagine.
    
If you would like to submit a pull request to this library, please read the [contributor guidelines](./CONTRIBUTING.md).

# TODO

Figure out how to bubble up the exception from the function/pipeline. function/base.py error method

Track down memory leak: https://www.fugue.co/blog/diagnosing-and-fixing-memory-leaks-in-python.html

Add `pandiocli performance --project_folder_name examples/form_fraud --dataset_name FormSubmissionGenerator --loops 1000` that will automatically profile the function and output recommendations. Check speed, memory, etc as it runs.

Maybe integrate this simulator? https://github.com/namebrandon/Sparkov_Data_Generation

Allow `Pipelines` to be built programmatically at runtime, to allow the potential for thousands to be built easily.

Fix storage mechanism storing things as a string. Pickle doesn't appear to be working.

Pulsar runs python function in a child process, cannot access the kill signal. Need another solution.

Schema is dynamically loaded from the config file, in the wrapper class, see if there is a better way to dynamically import this. pandioml.data.Submission instead of Submission, with pandioml.data hardcoded.

Pulsar is not importing the class files correctly, nor is it installing dependencies with Docker.

Getting cirulcar import errors with `data/__init__.py` line `from .stream import Stream` and `from .record import Record`

# Potential Datasets

./scripts/credit-card-fraud.arff - https://weka.8497.n7.nabble.com/file/n23121/credit_fruad.arff

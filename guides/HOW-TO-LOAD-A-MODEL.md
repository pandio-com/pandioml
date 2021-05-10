# How To Load A Model

Training a model can happen locally or on the Pandio platform.

By default, when deploying a pipeline to the Pandio platform, the model used starts fresh with no data trained.

To deploy to the Pandio platform with a trained model, place it inside of your project folder at the same level as the `function.py`. The name passed as the first argument below must match the filename exactly.

Then, utilize the `ModelUtility` class to load it in your `function.py`.

```buildoutcfg
class Function(FunctionBase):
    model = artifact.add('LinearRegression_model',
                         ModelUtility.load_or_instantiate('LinearRegression_model.pickle', LinearRegression))
```

The above example adds the model as an artifact, and utilizes the load or instantiate method of the ModelUtility class to either load an existing model or start a new model.

When using the `artifact.add` example above, your model will be automatically checkpointed and saved upon completion as a pickle file.

This is the file you'll want to copy into your project folder to deploy it to the Pandio platform.

## Versioning Models

The best way to version models is to utilize the artifacts functionality of PandioML. This saves a complete model that can be loaded at any future point.

The models saved by the artifact functionality are automatically versioned by time and the pipeline code used to generate it.

This gives you the ability to select the model you would like to deploy to the Pandio.com platform when training a model locally.

## Models Trained On Pandio's Platform

After a pipeline is deployed on Pandio's platform, an artifact will be stored periodically as the pipeline runs. This model can be downloaded from the Pandio platform from inside of the Dashboard, and then included in an additional pipeline as needed.
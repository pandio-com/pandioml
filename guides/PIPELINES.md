# Pipelines

This class was built as a container for pipelines, holding an internal list of individual pipelines with name references to each pipeline.

Its job is to provide an iterable list of pipelines to execute asynchronously.

Commonly, pipelines will be added manually with the `add` method.

For large pipelines, such as hypertuning thousands of parameters, a loop could be written to allow the programmatic creation of large number of pipelines.

```buildoutcfg
class Function(FunctionBase):
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

**Note:** Currently only one pipeline is supported. The first one defined will be executed. The ability to run multiple pipelines will be supported in the next release.

## Pipeline

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

## Important Note

All implementations in PandioML will always be an instance of Pipelines, even if only one Pipeline is being used. This allows Pandio's platform to perform optimizations.

## Example Pipeline

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
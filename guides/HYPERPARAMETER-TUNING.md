# Hyperparameter Tuning

The art of tuning a model can be a lot of fun. The times when it is not fun is when it takes a lot of time to iterate on the different parameters.

PandioML helps make this significantly easier by allowing any number of pipelines to be defined and executed all at once.

Take for example this pipeline:

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

Inside of PandioML we could modify this pipeline to be the following:

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
).add(
    'inference_wo_scale',
    Pipeline(*args, **kwargs)
        .then(self.feature_extraction)
        .then(self.label_extraction)
        .then(self.fit)
        .final(self.predict)
        .done(self.done)
        .catch(self.error)
)
```

The second pipeline added has the scale feature removed.

If we ran the second pipeline, we could see how having the scale impacts the model.

When defining the pipelines like above, these two pipelines will run concurrently.

Lets take it a bit further to tune the model more directly.

Again, here is the starting pipeline:

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

We could now add the ability to change the model parameters:

```buildoutcfg
p = Pipelines()
for i in range(0, 5):
    p.add(f"inference_{i}",
        Pipeline(*args, **kwargs)
            .then(self.set_model, AdaptiveRandomForestClassifier(
                    n_models=(3 + i),
                    seed=42
                ))
            .then(self.feature_extraction)
            .then(self.scale)
            .then(self.label_extraction)
            .then(self.fit)
            .final(self.predict)
            .done(self.done)
            .catch(self.error)
    )
```

The above example has created 5 pipelines which PandioML will run in parallel.

The results can then be compared to see which value of `n_models` provides the ideal desired metric.

## Thousands Of Pipelines

These examples show a small number of pipelines, but it is possible to run tens of thousands of pipelines in parallel.

By deploying the function to the Pandio.com platform through PandioML, there is no limit to the number of pipelines that could be run concurrently.

PandioML allows you to hypertune millions of parameters in your pipelines!

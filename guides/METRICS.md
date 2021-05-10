# Metrics

When a pipeline is executed, it is helpful to record metrics as it progresses.

This collection of classes allows metrics to be recorded easily.

These are most commonly used inside of a loop.

Each execution of `function.py` is done inside of a loop, so these metrics can be recorded easily inside of `function.py`.

A few examples are below. For details on the rest, view their class definitions.

## Accuracy

```buildoutcfg
from pandioml.metrics import Accuracy

metric = Accuracy()

metric = metric.update(label, prediction)

print(metric)
```
**Example Output**
```buildoutcfg
>>> Accuracy: 70.00%
```

## Jaccard

```buildoutcfg
from pandioml.metrics import Jaccard

metric = Jaccard()

metric = metric.update(label, prediction)

print(metric)
```
**Example Output**
```buildoutcfg
>>> Jaccard: 0.583333
```

## Precision

```buildoutcfg
from pandioml.metrics import Precision

metric = Precision()

metric = metric.update(label, prediction)

print(metric)
```
**Example Output**
```buildoutcfg
>>> Precision: 0.5
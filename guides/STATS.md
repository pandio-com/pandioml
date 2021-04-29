# Stats

When a pipeline is executed, it is helpful to record statistics as it progresses.

This collection of classes allows statistics to be recorded easily.

A few examples are below. For details on the rest, view their class definitions.

## Mean

```buildoutcfg
from pandioml.stats import Mean

stat = Mean()

stat = stat.update(5)

print(stat.get())
```
**Example Output**
```buildoutcfg
>>> 5.0
```
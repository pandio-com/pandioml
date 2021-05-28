# Lead Scoring Dataset

This example is found in [./examples/lead_scoring_dataset](./examples/lead_scoring_dataset) and streams lead submissions.

## Install

It is highly recommended to setup a virtual environment before installing PandioML.

This is an optional step before getting started.

`python -m venv /path/to/new/virtual/environment`

`pip install pandioml`

## Generate Project Template

`pandiocli dataset generate --project_name lead_scoring_dataset`

## Open Template File In Your Editor Of Choice

Let us create a dataset that will stream data into PandioML.

This dataset has the following schema:

In your editor, you will see these methods that need to be defined:

* `__init__`
* `next`
* `schema`

Let us create the following class with the necessary schema for this dataset.

```buildoutcfg
class Submission(Record):
    name = String()
    email = String()
    ip = String()
    timestamp = Integer()
```

Now, lets define the `__init__` method.

Most commonly, this establishes the dataset as an iterable so that the `next` method can iterate on it.

```buildoutcfg
def __init__(self):
    self.dataset = faker.Faker('en_US')
```

This dataset uses the Faker library to generate synthetic data.

All we have to do now is define the `next` method which returns an individual record.

```buildoutcfg
def next(self):
    return Submission(name=getattr(self.dataset, 'name')(), email=getattr(self.dataset, 'ascii_email')(), ip=getattr(self.dataset, 'ipv4')(),
                      timestamp=getattr(self.dataset, 'unix_time')())
```

Now our dataset is ready to be used!

## Full Example Code

```buildoutcfg
import faker
from pandioml.data.stream import Stream
from pandioml.data.record import JsonSchema, Record, String, Integer


class Dataset(Stream):
    """
    Web Form submission generator using the Faker class.

    Each record is an instance of Submission

    class Submission(Record):
        name = String()
        email = String()
        ip = String()
        timestamp = Float()
    """
    dataset = None

    def __init__(self):
        self.dataset = faker.Faker('en_US')

    def next(self):
        return Submission(name=getattr(self.dataset, 'name')(), email=getattr(self.dataset, 'ascii_email')(), ip=getattr(self.dataset, 'ipv4')(),
                          timestamp=getattr(self.dataset, 'unix_time')())

    @staticmethod
    def schema():
        return JsonSchema(Submission)


class Submission(Record):
    name = String()
    email = String()
    ip = String()
    timestamp = Integer()

```
# Credit Card Dataset

This example is found in [./examples/credit_card_dataset](./examples/credit_card_dataset) and streams transactions for credit card fraud.

## Install

It is highly recommended to setup a virtual environment before installing PandioML.

This is an optional step before getting started.

`python -m venv /path/to/new/virtual/environment`

`pip install pandioml`

## Generate Project Template

`pandiocli dataset generate --project_name credit_card_dataset`

## Open Template File In Your Editor Of Choice

Let us create a dataset that will stream data into PandioML.

This dataset has the following schema:

In your editor, you will see these methods that need to be defined:

* `__init__`
* `next`
* `schema`

The dataset in CSV format is found here: [https://pandio-com.github.io/static/files/datasets/creditcardfraud.zip](https://pandio-com.github.io/static/files/datasets/creditcardfraud.zip)

Let us create the following class with the necessary schema for this dataset.

```buildoutcfg
class Transaction(Record):
    Time = Float()
    V1 = Float()
    V2 = Float()
    V3 = Float()
    V4 = Float()
    V5 = Float()
    V6 = Float()
    V7 = Float()
    V8 = Float()
    V9 = Float()
    V10 = Float()
    V11 = Float()
    V12 = Float()
    V13 = Float()
    V14 = Float()
    V15 = Float()
    V16 = Float()
    V17 = Float()
    V18 = Float()
    V19 = Float()
    V20 = Float()
    V21 = Float()
    V22 = Float()
    V23 = Float()
    V24 = Float()
    V25 = Float()
    V26 = Float()
    V27 = Float()
    V28 = Float()
    Amount = Float()
    Class = Integer()
```

Now, lets define the `__init__` method.

Most commonly, this establishes the dataset as an iterable so that the `next` method can iterate on it.

```buildoutcfg
def __init__(self):
    self._download()
    self.dataset = iter(self._reader())
```

We've used this to make two method calls.

The first downloads the CSV if it hasn't already been downloaded.

```buildoutcfg
def _download(self):
    if not os.path.exists(self.path):
        import urllib
        import zipfile

        url = "https://pandio-com.github.io/static/files/datasets/creditcardfraud.zip"
        extract_dir = os.path.dirname(os.path.realpath(__file__))

        zip_path, _ = urllib.request.urlretrieve(url)
        with zipfile.ZipFile(zip_path, "r") as f:
            f.extractall(extract_dir)
```

The next establishes a CSV reader in a memory efficient way, reading only one record in at a time, instead of loading the entire file at once.

With streaming, this is an important distinction.

```buildoutcfg
def _reader(self):
    with open(self.path, 'r') as data:
        reader = csv.DictReader(data)
        for row in reader:
            yield row
```

Now our dataset is ready to be used!

## Full Example Code

```buildoutcfg
from pandioml.data.stream import Stream
from pandioml.data.record import JsonSchema, Record, Integer, Float
import csv
import os


class Dataset(Stream):
    """
    CSV template of credit card transactions with fraud.

    Each record is an instance of Transaction

    class Transaction(Record):
        Time = Float()
        V1 = Float()
        V2 = Float()
        V3 = Float()
        V4 = Float()
        V5 = Float()
        V6 = Float()
        V7 = Float()
        V8 = Float()
        V9 = Float()
        V10 = Float()
        V11 = Float()
        V12 = Float()
        V13 = Float()
        V14 = Float()
        V15 = Float()
        V16 = Float()
        V17 = Float()
        V18 = Float()
        V19 = Float()
        V20 = Float()
        V21 = Float()
        V22 = Float()
        V23 = Float()
        V24 = Float()
        V25 = Float()
        V26 = Float()
        V27 = Float()
        V28 = Float()
        Amount = Float()
        Class = Integer()
    """
    dataset = None
    path = os.path.dirname(os.path.realpath(__file__)) + '/creditcard.csv'

    def __init__(self):
        self._download()
        self.dataset = iter(self._reader())

    def _download(self):
        if not os.path.exists(self.path):
            import urllib
            import zipfile

            url = "https://pandio-com.github.io/static/files/datasets/creditcardfraud.zip"
            extract_dir = os.path.dirname(os.path.realpath(__file__))

            zip_path, _ = urllib.request.urlretrieve(url)
            with zipfile.ZipFile(zip_path, "r") as f:
                f.extractall(extract_dir)

    def _reader(self):
        with open(self.path, 'r') as data:
            reader = csv.DictReader(data)
            for row in reader:
                yield row

    def next(self):
        row = next(self.dataset)
        _data = {}
        for key in row.keys():
            if key == 'Class':
                _data[key] = int(row[key])
            else:
                _data[key] = float(row[key])
        return Transaction(**_data)

    @staticmethod
    def schema():
        return JsonSchema(Transaction)


class Transaction(Record):
    Time = Float()
    V1 = Float()
    V2 = Float()
    V3 = Float()
    V4 = Float()
    V5 = Float()
    V6 = Float()
    V7 = Float()
    V8 = Float()
    V9 = Float()
    V10 = Float()
    V11 = Float()
    V12 = Float()
    V13 = Float()
    V14 = Float()
    V15 = Float()
    V16 = Float()
    V17 = Float()
    V18 = Float()
    V19 = Float()
    V20 = Float()
    V21 = Float()
    V22 = Float()
    V23 = Float()
    V24 = Float()
    V25 = Float()
    V26 = Float()
    V27 = Float()
    V28 = Float()
    Amount = Float()
    Class = Integer()

```
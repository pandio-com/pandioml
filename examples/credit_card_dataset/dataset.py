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

from pandioml.data.stream import Stream
from pandioml.data.record import JsonSchema, Record, String, Integer, Double
import csv
import os


class Dataset(Stream):
    """
    CSV template showing how to load a CSV and stream the records in.

    Each record is an instance of Transaction

    class Transaction(Record):
        id = String()
        amount = Double()
        timestamp = Integer()
    """
    dataset = None
    path = os.path.dirname(os.path.realpath(__file__)) + '/data.csv'

    def __init__(self):
        self.dataset = iter(self._reader())

    def _reader(self):
        with open(self.path, 'r') as data:
            reader = csv.reader(data)
            for row in reader:
                yield row

    def next(self):
        row = next(self.dataset)
        return Transaction(id=row[0], amount=float(row[1]), timestamp=int(row[2]))

    @staticmethod
    def schema():
        return JsonSchema(Transaction)


class Transaction(Record):
    id = String()
    amount = Double()
    timestamp = Integer()

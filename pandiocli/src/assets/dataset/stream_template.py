from pandioml.data.stream import Stream
from pandioml.data.record import JsonSchema, Record, String, Integer, Double


class Dataset(Stream):
    """
    Dataset template showing how to stream the records in.

    Each record is an instance of Transaction

    class Transaction(Record):
        id = String()
        amount = Double()
        timestamp = Integer()
    """
    dataset = None

    def __init__(self):
        self.dataset = iter([{
            'id': '1',
            'amount': 2.50,
            'timestamp': 123456789
        }])

    def next(self):
        return Transaction(**next(self.dataset))

    @staticmethod
    def schema():
        return JsonSchema(Transaction)


class Transaction(Record):
    id = String()
    amount = Double()
    timestamp = Integer()

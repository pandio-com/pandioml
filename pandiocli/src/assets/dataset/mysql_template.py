from pandioml.data.stream import Stream
from pandioml.data.record import JsonSchema, Record, String, Integer, Double
import mysql.connector


class Dataset(Stream):
    """
    MySQL template showing how to connect to a database and stream the records in.

    Each record is an instance of Transaction

    class Transaction(Record):
        id = String()
        amount = Double()
        timestamp = Integer()
    """
    conn = None
    dataset = None

    def __init__(self):
        self.conn = mysql.connector.connect(
          host="localhost",
          user="yourusername",
          password="yourpassword",
          database="mydatabase"
        )
        self.dataset = self.conn.cursor()
        self.dataset.execute('SELECT * FROM transactions')

    def next(self):
        row = self.dataset.fetchone()
        return Transaction(id=row[1], amount=row[2], timestamp=row[3])

    @staticmethod
    def schema():
        return JsonSchema(Transaction)


class Transaction(Record):
    id = String()
    amount = Double()
    timestamp = Integer()

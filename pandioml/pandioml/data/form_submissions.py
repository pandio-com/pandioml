import faker
from pandioml.data.stream import Stream
from pandioml.data.record import JsonSchema, Record, String, Integer


class FormSubmissionGenerator(Stream):
    """
    Web Form submission generator using the Faker class.

    Each record is an instance of Submission

    class Submission(Record):
        email = String()
        ip = String()
        timestamp = Float()
    """

    def __init__(self):
        self.fake = faker.Faker('en_US')

    def next(self):
        return Submission(email=getattr(self.fake, 'ascii_email')(), ip=getattr(self.fake, 'ipv4')(),
                          timestamp=getattr(self.fake, 'unix_time')())

    @staticmethod
    def schema():
        return JsonSchema(Submission)


class Submission(Record):
    email = String()
    ip = String()
    timestamp = Integer()

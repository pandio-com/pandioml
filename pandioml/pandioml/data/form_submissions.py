from pandioml.data.stream import Stream
import faker
from pandioml.data.record import Record, String, Integer


class FormSubmissionGenerator(Stream):
    def __init__(self):
        super().__init__()

        self.fake = faker.Faker('en_US')

    """
    Each record is an instance of Submission
    
    class Submission(Record):
        email = String()
        ip = String()
        timestamp = Float()
    """
    def next(self):
        return Submission(email=getattr(self.fake, 'ascii_email')(), ip=getattr(self.fake, 'ipv4')(),
                          timestamp=getattr(self.fake, 'unix_time')())

    def help(self):
        return """
        Each record is an instance of Submission
    
        class Submission(Record):
            email = String()
            ip = String()
            timestamp = Float()
        """


class Submission(Record):
    email = String()
    ip = String()
    timestamp = Integer()

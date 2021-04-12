from pandioml.data.stream import Stream
import faker
from pandioml.data.record import Record, String, Integer


class PersonProfileGenerator(Stream):
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
        pp = PersonProfile
        for attr in filter(lambda a: not a.startswith('__'), dir(PersonProfile)):
            pp[attr] = getattr(self.fake, attr)()

        return pp

    def help(self):
        return """
        Each record is an instance of Submission
    
        class Submission(Record):
            email = String()
            ip = String()
            timestamp = Float()
        """


class PersonProfile(Record):
    ascii_email = String()
    ipv4 = String()
    unix_time = Integer()

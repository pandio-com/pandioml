from pandioml.data.stream import Stream
import faker
from pandioml.data.record import Record, String, Integer


class PersonProfileGenerator(Stream):
    """
    A generator to produce an infinite amount of Person profiles using the Faker class.

    Each record is an instance of PersonProfile

    class PersonProfile(Record):
        ascii_email = String()
        ipv4 = String()
        unix_time = Integer()
    """

    def __init__(self):
        super().__init__()

        self.fake = faker.Faker('en_US')

    def next(self):
        pp = PersonProfile
        for attr in filter(lambda a: not a.startswith('__'), dir(PersonProfile)):
            pp[attr] = getattr(self.fake, attr)()

        return pp


class PersonProfile(Record):
    ascii_email = String()
    ipv4 = String()
    unix_time = Integer()

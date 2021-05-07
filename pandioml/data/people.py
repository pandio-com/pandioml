from pandioml.data.stream import Stream
import faker
from pandioml.data.record import JsonSchema, Record, String, Integer, Float
from decimal import Decimal


class PersonProfileGenerator(Stream):
    """
    A generator to produce an infinite amount of Person profiles using the Faker class.

    Each record is an instance of PersonProfile

    class PersonProfile(Record):
        first_name_nonbinary = String()
        last_name_nonbinary = String()
        address = String()
        ascii_email = String()
        user_name = String()
        language_name = String()
        latitude = Float()
        longitude = Float()
        ssn = String()
        ipv4 = String()
        unix_time = Integer()
    """
    dataset = None

    def __init__(self):
        self.dataset = faker.Faker('en_US')

    def next(self):
        _data = {}

        for attr in PersonProfile._fields.keys():
            _data[attr] = getattr(self.dataset, attr)()
            if isinstance(_data[attr], Decimal):
                _data[attr] = float(_data[attr])

        return PersonProfile(**_data)

    @staticmethod
    def schema():
        return JsonSchema(PersonProfile)


class PersonProfile(Record):
    first_name_nonbinary = String()
    last_name_nonbinary = String()
    address = String()
    ascii_email = String()
    user_name = String()
    language_name = String()
    latitude = Float()
    longitude = Float()
    ssn = String()
    ipv4 = String()
    unix_time = Integer()

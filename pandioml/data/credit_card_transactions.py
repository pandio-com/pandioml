from pandioml.data.stream import Stream
import pulsar
from pandioml.data.record import Record, String, Integer, Float, JsonSchema


class CreditCardFraud(Stream):
    """
    A dataset of 1,296,675 credit card transactions with a percentage labeled as fraud.

    Each record is an instance of Transaction

    class Transaction(Record):
        trans_date_trans_time = String()
        cc_num = Integer()
        merchant = String()
        category = String()
        amt = Float()
        first = String()
        last = String()
        gender = String()
        street = String()
        city = String()
        state = String()
        zip = Integer()
        lat = Float()
        long = Float()
        city_pop = Integer()
        job = String()
        dob = String()
        trans_num = String()
        unix_time = Integer()
        merch_lat = Float()
        merch_long = Float()
        is_fraud = Integer()
        weekday = Integer()
        weekend = Integer()
        month = Integer()
        day = Integer()
        hour = Integer()
    """
    index = 0
    dataset = None

    def __init__(self, start_id=pulsar.MessageId.earliest, receiver_queue_size = 1000, pandio_token=None):
        self.client = pulsar.Client('pulsar+ssl://joshuaeric--gray-guan.us-west2.gcp.pulsar.pandio.com:6651',
                                    authentication=pulsar.AuthenticationToken(pandio_token))

        self.reader = self.client.create_reader('persistent://public/default/credit-card-fraud', start_id,
                                                schema=JsonSchema(Transaction),
                                                receiver_queue_size=receiver_queue_size)

    def next(self):
        msg = self.reader.read_next()
        self.index += 1
        return msg

    @staticmethod
    def schema():
        return JsonSchema(Transaction)


class Transaction(Record):
    trans_date_trans_time = String()
    cc_num = Integer()
    merchant = String()
    category = String()
    amt = Float()
    first = String()
    last = String()
    gender = String()
    street = String()
    city = String()
    state = String()
    zip = Integer()
    lat = Float()
    long = Float()
    city_pop = Integer()
    job = String()
    dob = String()
    trans_num = String()
    unix_time = Integer()
    merch_lat = Float()
    merch_long = Float()
    is_fraud = Integer()
    weekday = Integer()
    weekend = Integer()
    month = Integer()
    day = Integer()
    hour = Integer()

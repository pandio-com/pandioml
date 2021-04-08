from pandioml.data.stream import Stream
import pulsar
from pulsar.schema import Record, String, Integer, Float, JsonSchema


class CreditCardFraud(Stream):
    index = 0
    start_id = 0
    end_id = -1
    count = 20000

    def __init__(self, start_id=0, end_id=-1):
        super().__init__()
        self.client = pulsar.Client('pulsar+ssl://joshuaeric--gray-guan.us-west2.gcp.pulsar.pandio.com:6651',
                                    authentication=pulsar.AuthenticationToken(pandio_token))

        receiver_queue_size = 1000
        if end_id > start_id:
            diff = end_id - start_id
            if diff < receiver_queue_size:
                receiver_queue_size = diff

        self.reader = self.client.create_reader('persistent://public/default/credit-card-fraud', start_id,
                                                schema=JsonSchema(Transaction),
                                                receiver_queue_size=receiver_queue_size)
        self.start_id = start_id
        self.end_id = end_id

    """
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

    def next(self):
        if self.index > self.end_id and self.end_id != -1:
            return None

        msg = self.reader.read_next()
        self.index += 1
        return msg

    def help(self):
        return """
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

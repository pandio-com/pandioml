from pandioml.data.stream import Stream
from pandioml.data.record import Record, Integer, Float
from river.datasets import Phishing


class PhisingDataset(Stream):
    """
    This dataset contains features from web pages that are classified as phishing or not.

    Each record is an instance of Webpage

    class Webpage(Record):
        empty_server_form_handler = Float()
        popup_window = Float()
        https = Float()
        request_from_other_domain = Float()
        anchor_from_other_domain = Float()
        is_popular = Float()
        long_url = Float()
        age_of_domain = Integer()
        ip_in_url = Integer()
        label = Integer()
    """

    def __init__(self):
        self.data = Phishing()
        self.dataset = iter(self.data)

    def next(self):
        X, Y = next(self.dataset)
        r = Webpage(**X)
        r.label = int(Y)
        return r


class Webpage(Record):
    empty_server_form_handler = Float()
    popup_window = Float()
    https = Float()
    request_from_other_domain = Float()
    anchor_from_other_domain = Float()
    is_popular = Float()
    long_url = Float()
    age_of_domain = Integer()
    ip_in_url = Integer()
    label = Integer()

from pandioml.data.stream import Stream
from pandioml.data.record import JsonSchema, Record, Integer, String, Boolean, Double, Float
from river.datasets import Restaurants
from datetime import datetime


class RestaurantVisitorsDataset(Stream):
    """
    This dataset contains 252,108 records over a 16 week period to 829 Japanese Restaurants.

    Each record is an instance of RestaurantDay

    class RestaurantDay(Record):
        store_id = String()
        timestamp = Float()
        is_holiday = Boolean()
        genre_name = String()
        area_name = String()
        latitude = Double()
        longitude = Double()
        visitors = Integer()
    """
    dataset = None

    def __init__(self):
        self.dataset = iter(Restaurants())

    def next(self):
        X, Y = next(self.dataset)
        return RestaurantDay(store_id=X['store_id'], timestamp=datetime.timestamp(X['date']),
                             is_holiday=X['is_holiday'], genre_name=X['genre_name'], area_name=X['area_name'],
                             latitude=X['latitude'], longitude=X['longitude'], visitors=Y)

    @staticmethod
    def schema():
        return JsonSchema(RestaurantDay)


class RestaurantDay(Record):
    store_id = String()
    timestamp = Float()
    is_holiday = Boolean()
    genre_name = String()
    area_name = String()
    latitude = Double()
    longitude = Double()
    visitors = Integer()

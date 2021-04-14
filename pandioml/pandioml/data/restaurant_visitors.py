from pandioml.data.stream import Stream
from pandioml.data.record import Record, Integer, String, Boolean, Double, Float
from river.datasets import Restaurants
from datetime import datetime


class RestaurantVisitorsDataset(Stream):
    """
    This dataset contains 252,108 records over a 16 week period to 829 Japanese Restaurants.

    Each record is an instance of MovieRating

    class MovieRating(Record):
        user_id = Integer()
        item_id = Integer()
        timestamp = Integer()
        title = String()
        release_date = Integer()
        genres = String()
        user_age = Integer()
        user_gender = String()
        user_occupation = String()
        user_zip_code = Integer()
        user_movie_rating = Float()
    """
    def __init__(self):
        self.data = Restaurants()
        self.dataset = iter(self.data)

    def next(self):
        X, Y = next(self.dataset)
        return RestaurantDay(store_id=X['store_id'], timestamp=datetime.timestamp(X['date']),
                             is_holiday=X['is_holiday'], genre_name=X['genre_name'], area_name=X['area_name'],
                             latitude=X['latitude'], longitude=X['longitude'], visitors=Y)


class RestaurantDay(Record):
    store_id = String()
    timestamp = Float()
    is_holiday = Boolean()
    genre_name = String()
    area_name = String()
    latitude = Double()
    longitude = Double()
    visitors = Integer()

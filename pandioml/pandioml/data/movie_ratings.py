from pandioml.data.stream import Stream
from pandioml.data.record import Record, Integer, Float, String
from river.datasets import MovieLens100K


class MovieRatingDataset(Stream):
    """
    This dataset contains 100,000 movie ratings from a variety of individuals.

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
        self.data = MovieLens100K()
        self.dataset = iter(self.data)

    def next(self):
        X, Y = next(self.dataset)
        return MovieRating(user_id = int(X['user']), item_id = int(X['item']), timestamp=X['timestamp'],
                           title=X['title'], release_date=X['release_date'], genres=X['genres'], user_age=int(X['age']),
                           user_gender=X['gender'], occupation=X['occupation'], user_zip_code=int(X['zip_code']),
                           user_movie_rating=Y)


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

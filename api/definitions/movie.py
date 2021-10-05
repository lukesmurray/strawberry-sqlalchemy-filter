import strawberry
from api.definitions.director import Director
from main.sqlmodels import Movie as MovieModel


@strawberry.experimental.pydantic.type(
    model=MovieModel,
    fields=[
        "id",
        "title",
        "imdb_id",
        "year",
        "image_url",
        "imdb_rating",
        "imdb_rating_count",
        "director_id",
        "director",
    ],
)
class Movie:
    director: Director

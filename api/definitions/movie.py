from typing import Optional

import strawberry
from api.definitions.director import Director, DirectorInput
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


@strawberry.experimental.pydantic.input(
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
class MovieInput:
    director: Optional[DirectorInput]

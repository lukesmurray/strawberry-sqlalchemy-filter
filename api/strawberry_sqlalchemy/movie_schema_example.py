import typing as t

import strawberry
from api.strawberry_sqlalchemy.schema_generation import (
    create_array_relationship_type,
    create_generation_context,
    create_query_root,
)
from main.database import engine
from sqlmodel import Session
from strawberry.extensions import Extension

from .movie_model_example import DirectorModel, MovieModel


class SQLAlchemySession(Extension):
    def on_request_start(self):
        self.execution_context.context["db"] = Session(
            autocommit=False, autoflush=False, bind=engine, future=True
        )

    def on_request_end(self):
        self.execution_context.context["db"].close()


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
    ],
)
class Movie:
    pass


@strawberry.experimental.pydantic.type(
    model=DirectorModel,
    fields=["id", "name", "movies"],
)
class Director:
    movies: t.List[Movie] = strawberry.field(
        resolver=create_array_relationship_type(Movie)
    )


auto_types = [Movie, Director]
auto_schema_context = create_generation_context(auto_types)


class AutoSchemaContext(Extension):
    def on_request_start(self):
        self.execution_context.context["auto_schema"] = auto_schema_context


Query = create_query_root(auto_types)

schema = strawberry.Schema(
    query=Query, extensions=[SQLAlchemySession, AutoSchemaContext]
)

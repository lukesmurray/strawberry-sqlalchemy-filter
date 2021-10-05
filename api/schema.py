from typing import List

import strawberry
from main.database import SessionLocal
from main.sqlmodels import get_movies
from strawberry.extensions import Extension

from .definitions.movie import Movie


class SQLAlchemySession(Extension):
    def on_request_start(self):
        self.execution_context.context["db"] = SessionLocal()

    def on_request_end(self):
        self.execution_context.context["db"].close()


@strawberry.type
class Query:
    @strawberry.field
    def top_rated_movies(self, info, limit: int = 250) -> List[Movie]:
        db = info.context["db"]
        movies = get_movies(db, limit=limit)
        return [Movie.from_pydantic(movie) for movie in movies]


schema = strawberry.Schema(Query, extensions=[SQLAlchemySession])

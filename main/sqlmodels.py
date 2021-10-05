from typing import Optional

from sqlalchemy import desc, select
from sqlalchemy.orm import Session, joinedload
from sqlmodel import Field, SQLModel
from sqlmodel.main import Relationship


class Director(SQLModel, table=True):
    __tablename__ = "directors"

    id: Optional[int] = Field(
        default=None, primary_key=True, index=True, nullable=False
    )
    # missing unique constraint https://github.com/tiangolo/sqlmodel/pull/83/files
    name: str = Field(default=None, index=True, nullable=False)


class Movie(SQLModel, table=True):
    __tablename__ = "movies"

    id: int = Field(default=None, primary_key=True, index=True, nullable=False)
    # missing unique constraint https://github.com/tiangolo/sqlmodel/pull/83/files
    title: str = Field(default=None, nullable=False)
    # missing unique constraint https://github.com/tiangolo/sqlmodel/pull/83/files
    imdb_id: str = Field(default=None, index=True, nullable=False)
    year: int = Field(default=None, nullable=False)
    image_url: str = Field(default=None, nullable=False)
    imdb_rating: float = Field(default=None, nullable=False)
    imdb_rating_count: str = Field(default=None, nullable=False)
    director_id: int = Field(default=None, foreign_key="directors.id", nullable=False)
    director: Director = Relationship()


def get_movies(db: Session, limit: int = 250):
    query = (
        select(Movie)
        .options(joinedload(Movie.director))
        .order_by(desc(Movie.imdb_rating))
        .limit(limit)
    )

    result = db.execute(query).unique()
    return result.scalars()

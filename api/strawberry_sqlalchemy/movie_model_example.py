import typing as t

from sqlmodel import Field, Relationship, SQLModel


class DirectorModel(SQLModel, table=True):
    __tablename__ = "directors"

    id: t.Optional[int] = Field(
        default=None, primary_key=True, index=True, nullable=False
    )
    # missing unique constraint https://github.com/tiangolo/sqlmodel/pull/83/files
    name: str = Field(default=None, index=True, nullable=False)
    movies: t.List["MovieModel"] = Relationship(back_populates="director")


class MovieModel(SQLModel, table=True):
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
    director_id: t.Optional[int] = Field(
        default=None, foreign_key="directors.id", nullable=True
    )
    director: t.Optional[DirectorModel] = Relationship(back_populates="movies")

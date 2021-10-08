from __future__ import annotations

import typing as t

import strawberry
from sqlmodel import Field, SQLModel

from .filter_generators import create_query_root


# define a database model
class UserModel(SQLModel, table=True):
    __tablename__ = "users"
    id: t.Optional[int] = Field(
        default=None, primary_key=True, index=True, nullable=False
    )
    age: int
    password: t.Optional[str]


# define a strawberry type
@strawberry.experimental.pydantic.type(UserModel, fields=["id", "age", "password"])
class User:
    pass


# pass the strawberry types you want to automatically query for
Query = create_query_root([User])

# create the schema
schema = strawberry.Schema(query=Query)

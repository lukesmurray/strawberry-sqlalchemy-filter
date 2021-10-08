from __future__ import annotations

import typing as t

import pydantic
import strawberry

from .filter_generators import create_query_root


# define a database model
class UserModel(pydantic.BaseModel):
    age: int
    password: t.Optional[str]


# define a strawberry type
@strawberry.experimental.pydantic.type(UserModel, fields=["age", "password"])
class User:
    pass


# pass the strawberry types you want to automatically query for
Query = create_query_root([User])

# create the schema
schema = strawberry.Schema(query=Query)

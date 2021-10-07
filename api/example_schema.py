from __future__ import annotations

import typing as t

import pydantic
import strawberry

from .strawberry_sqlalchemy.filter_generators import create_class_filter


# define a database model
class UserModel(pydantic.BaseModel):
    age: int
    password: t.Optional[str]


# define a strawberry type
@strawberry.experimental.pydantic.type(UserModel, fields=["age", "password"])
class User:
    pass


# create filters for the type
UserFilter = create_class_filter(User)


@strawberry.type
class Query:
    # use the filters in a query
    @strawberry.field
    def all_users(self, info, filter: UserFilter) -> t.List[User]:
        return [User(age=10, password="foo")]


schema = strawberry.Schema(Query)

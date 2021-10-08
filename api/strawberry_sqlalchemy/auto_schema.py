from __future__ import annotations

import typing as t

import strawberry
from sqlmodel import Field, Relationship, SQLModel

from .filter_generators import create_query_root


class AddressModel(SQLModel, table=True):
    __tablename__ = "addresses"
    id: t.Optional[int] = Field(
        default=None, primary_key=True, index=True, nullable=False
    )
    street: str
    state: str
    country: str
    zip: str
    users: t.List["UserModel"] = Relationship(back_populates="address")


class UserModel(SQLModel, table=True):
    __tablename__ = "users"
    id: t.Optional[int] = Field(
        default=None, primary_key=True, index=True, nullable=False
    )
    age: int
    password: t.Optional[str]
    address_id: t.Optional[int] = Field(default=None, foreign_key="addresses.id")
    address: t.Optional[AddressModel] = Relationship(back_populates="users")


@strawberry.experimental.pydantic.type(
    UserModel, fields=["id", "age", "password", "address_id", "address"]
)
class User:
    pass


@strawberry.experimental.pydantic.type(
    AddressModel, fields=["id", "street", "state", "country", "zip"]
)
class Address:
    users: t.List["User"] = None


Query = create_query_root([User, Address])

# create the schema
schema = strawberry.Schema(query=Query)

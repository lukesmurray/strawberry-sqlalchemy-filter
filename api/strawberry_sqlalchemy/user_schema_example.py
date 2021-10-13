from __future__ import annotations

import typing as t

import strawberry
from sqlmodel import Field, Relationship, SQLModel

from .schema_generation import create_array_relationship_type, create_query_root


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
    users: t.List[create_array_relationship_type(User)] = strawberry.field(
        resolver=create_array_relationship_type(User)
    )


Query = create_query_root([User, Address])

schema = strawberry.Schema(query=Query)

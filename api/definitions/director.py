import strawberry
from main.sqlmodels import Director as DirectorModel


@strawberry.experimental.pydantic.type(
    model=DirectorModel,
    fields=[
        "id",
        "name",
    ],
)
class Director:
    pass


@strawberry.experimental.pydantic.input(
    model=DirectorModel,
    fields=[
        "id",
        "name",
    ],
)
class DirectorInput:
    pass

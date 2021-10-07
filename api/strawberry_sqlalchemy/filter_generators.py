import dataclasses
import typing as t
from types import SimpleNamespace

import strawberry


class Op(SimpleNamespace):
    eq = "eq"
    neq = "neq"
    lt = "lt"
    lte = "lte"
    gt = "gt"
    gte = "gte"

    contains = "contains"
    not_contains = "not_contains"

    in_ = "in_"
    not_in = "not_in"


_OP_COMPARISONS = {Op.eq, Op.neq, Op.lt, Op.lte, Op.gt, Op.gte}

_SAME_TYPE_OP = _OP_COMPARISONS
_INCLUSION_OP = {Op.in_, Op.not_in}
_CONTAINS_OP = {Op.contains, Op.not_contains}

FILTER_MAP: dict[type, set[str]] = {
    bool: {Op.eq, Op.neq},
    int: {*_OP_COMPARISONS, *_INCLUSION_OP},
    str: {*_OP_COMPARISONS, *_INCLUSION_OP, *_CONTAINS_OP},
    set: {*_CONTAINS_OP},
    list: {*_CONTAINS_OP},
}


def create_filter_name(type_):
    generics = t.get_args(type_)
    return (
        "".join(g.__name__.capitalize() for g in generics)
        + type_.__name__.capitalize()
        + "Filter"
    )


def create_scalar_filter(type_: type):
    operations = FILTER_MAP[t.get_origin(type_) or type_]
    fields = []
    for op in operations:
        if op in _SAME_TYPE_OP:
            fields.append((op, t.Optional[type_], dataclasses.field(default=None)))

        elif op in _INCLUSION_OP:
            fields.append(
                (op, t.Optional[t.List[type_]], dataclasses.field(default=None))
            )

        elif op in _CONTAINS_OP:
            generic_args = t.get_args(type_)
            container_type = t.get_origin(type_) or type_

            if len(generic_args) == 1:
                resulting_type = t.Optional[container_type[generic_args[0]]]
            else:
                resulting_type = t.Optional[container_type]

            fields.append((op, resulting_type, dataclasses.field(default=None)))
    filter_ = dataclasses.make_dataclass(create_filter_name(type_), fields=fields)
    return strawberry.input(filter_)


def create_class_filter(type_: type):
    def is_optional(field):
        return t.get_origin(field) is t.Union and type(None) in t.get_args(field)

    def unwrap_optional(field):
        if is_optional(field):
            if len(t.get_args(field)) > 2:
                raise ValueError(
                    "Unable to filter fields which may contain multiple types "
                    + f"of scalars: {field}"
                )
            return [t_ for t_ in t.get_args(field) if t_ is not None][0]
        return field

    type_hints = t.get_type_hints(type_)
    class_name = f"{type_.__name__}Filter"
    globals()[class_name] = dataclasses.make_dataclass(
        class_name,
        fields=[
            *[
                (
                    field_name,
                    create_scalar_filter(unwrap_optional(field_type)),
                    dataclasses.field(default=None),
                )
                for field_name, field_type in type_hints.items()
            ],
            *[
                ("and_", t.Optional[class_name], dataclasses.field(default=None)),
                ("or_", t.Optional[class_name], dataclasses.field(default=None)),
            ],
        ],
        namespace={"__module__": __name__},
    )
    return strawberry.input(globals()[class_name])

import dataclasses
import typing as t
from types import SimpleNamespace

import strawberry


class BoolOps(SimpleNamespace):
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

    is_null_ = "is_null"


_BOOL_OP_COMPARISONS = {
    BoolOps.eq,
    BoolOps.neq,
    BoolOps.lt,
    BoolOps.lte,
    BoolOps.gt,
    BoolOps.gte,
}

_SAME_TYPE_BOOL_OP = _BOOL_OP_COMPARISONS
_INCLUSION_BOOL_OP = {BoolOps.in_, BoolOps.not_in}
_CONTAINS_BOOL_OP = {BoolOps.contains, BoolOps.not_contains}

_SCALAR_BOOL_OP_MAP: dict[type, set[str]] = {
    bool: {BoolOps.eq, BoolOps.neq},
    int: {*_BOOL_OP_COMPARISONS, *_INCLUSION_BOOL_OP},
    str: {*_BOOL_OP_COMPARISONS, *_INCLUSION_BOOL_OP, *_CONTAINS_BOOL_OP},
    set: {*_CONTAINS_BOOL_OP},
    list: {*_CONTAINS_BOOL_OP},
}


def is_optional(type_):
    """Check if a type is optional. For example t.Optional[int] is optional,"""
    return t.get_origin(type_) is t.Union and type(None) in t.get_args(type_)


def unwrap_optional(type_):
    """Return the non optional version of a type. For example t.Optional[int]
    would return int.
    """
    if is_optional(type_):
        if len(t.get_args(type_)) > 2:
            raise ValueError(
                "Unable to filter fields which may contain multiple types "
                + f"of scalars: {type_}"
            )
        return [t_ for t_ in t.get_args(type_) if t_ is not None][0]
    return type_


def create_comparison_expression_name(type_):
    generics = t.get_args(type_)
    return (
        "".join(g.__name__.capitalize() for g in generics)
        + type_.__name__.capitalize()
        + "Filter"
    )


def create_scalar_comparison_expression(type_: type):
    type_ = unwrap_optional(type_)
    operations = _SCALAR_BOOL_OP_MAP[t.get_origin(type_) or type_]
    fields = []
    for op in operations:
        if op in _SAME_TYPE_BOOL_OP:
            fields.append((op, t.Optional[type_], dataclasses.field(default=None)))

        elif op in _INCLUSION_BOOL_OP:
            fields.append(
                (op, t.Optional[t.List[type_]], dataclasses.field(default=None))
            )

        elif op in _CONTAINS_BOOL_OP:
            generic_args = t.get_args(type_)
            container_type = t.get_origin(type_) or type_

            if len(generic_args) == 1:
                resulting_type = t.Optional[container_type[generic_args[0]]]
            else:
                resulting_type = t.Optional[container_type]

            fields.append((op, resulting_type, dataclasses.field(default=None)))

    # TODO: would be nice to only add is_null if the field is optional.
    # but we would need to change the `expression_name` since we register
    # the expression as a global and whichever class we define last will
    # override prior classes
    fields.append((BoolOps.is_null_, t.Optional[bool], dataclasses.field(default=None)))

    expression_name = create_comparison_expression_name(type_)
    globals()[expression_name] = dataclasses.make_dataclass(
        expression_name,
        fields=fields,
        namespace={"__module__": __name__},
    )
    return strawberry.input(globals()[expression_name])


def create_non_scalar_comparison_expression(type_: type):

    type_hints = t.get_type_hints(type_)
    fields = []
    expression_name = create_comparison_expression_name(type_)
    for field_name, field_type in type_hints.items():
        fields.append(
            (
                field_name,
                create_scalar_comparison_expression(field_type),
                dataclasses.field(default=None),
            )
        )
    fields.append(
        ("and_", t.Optional[expression_name], dataclasses.field(default=None)),
    )
    fields.append(
        ("or_", t.Optional[expression_name], dataclasses.field(default=None)),
    )
    globals()[expression_name] = dataclasses.make_dataclass(
        expression_name,
        fields=fields,
        namespace={"__module__": __name__},
    )
    return strawberry.input(globals()[expression_name])


def create_all_type_query_name(type_):
    type_name = type_.__name__.capitalize()
    if not type_name.endswith("s"):
        type_name += "s"
    return f"all_{type_name}"


def create_all_type_query_field(type_: type):
    method_name = create_all_type_query_name(type_)

    def all_type_query_implementation(
        self,
        info,
        where: t.Optional[create_non_scalar_comparison_expression(type_)] = None,
        limit: t.Optional[int] = None,
        offset: t.Optional[int] = None,
    ) -> t.List[type_]:
        # TODO: actually implement the query
        return [type_(age=10, password="foo")]

    return (
        method_name,
        t.List[type_],
        dataclasses.field(default=strawberry.field(all_type_query_implementation)),
    )


def create_query_root(types: t.List[type]):

    all_type_queries = [create_all_type_query_field(type_) for type_ in types]

    query_root_name = "query_root"
    globals()[query_root_name] = dataclasses.make_dataclass(
        query_root_name,
        fields=[*all_type_queries],
        namespace={
            **{"__module__": __name__},
        },
    )

    return strawberry.type(globals()[query_root_name])

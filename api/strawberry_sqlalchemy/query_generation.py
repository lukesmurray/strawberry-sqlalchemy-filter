import typing as t

from sqlalchemy.orm import RelationshipProperty, selectinload
from sqlmodel import select


def get_schema_context(info):
    schema_context = info.context["auto_schema"]
    return schema_context


def get_model_for_type(info, type_):
    schema_context = get_schema_context(info)
    model = schema_context["type_to_model"][type_]
    return model


def get_strawberry_fields_for_type(info, type_):
    schema_context = get_schema_context(info)
    strawberry_fields = schema_context["type_to_type_definition"][type_].fields
    return strawberry_fields


def get_mapper_for_column(info, column):
    return column.property.mapper


def get_type_for_column(info, column):
    schema_context = get_schema_context(info)
    return schema_context["mapper_to_type"][get_mapper_for_column(info, column)]


def get_graphql_python_name_map_for_type(info, type_):
    """Create a mapping from graphql field names to python attribute names"""

    strawberry_fields = get_strawberry_fields_for_type(info, type_)
    name_map = {
        f.get_graphql_name(info.schema.config.auto_camel_case): f.python_name
        for f in strawberry_fields
    }
    return name_map


def get_selected_field_columns(info, type_, selected_fields, model=None):

    model = get_model_for_type(info, type_) if model is None else model

    name_map = get_graphql_python_name_map_for_type(info, type_)
    selected_field_columns = [
        (s, getattr(model, name_map[s.name])) for s in selected_fields
    ]

    return selected_field_columns


def get_selected_scalar_non_scalar_field_columns(
    info, type_, selected_fields, model=None
):
    selected_field_columns = get_selected_field_columns(
        info, type_, selected_fields, model
    )

    scalar_field_columns = [
        fc
        for fc in selected_field_columns
        if not isinstance(fc[1].property, RelationshipProperty)
    ]

    non_scalar_field_columns = [
        c
        for c in selected_field_columns
        if isinstance(c[1].property, RelationshipProperty)
    ]

    return scalar_field_columns, non_scalar_field_columns


def do_nested_select(info, type_, query, selected_field, column, parent_model):
    selected_fields = [s for s in selected_field.selections]

    model = get_model_for_type(info, type_)
    (
        scalar_field_columns,
        non_scalar_field_columns,
    ) = get_selected_scalar_non_scalar_field_columns(
        info, type_, selected_fields, model
    )

    # TODO: selectinload is good for one to many relationships because it does
    # not create cartesian product issues.
    # https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html#what-kind-of-loading-to-use
    # however we probably want joined loading for many to one relationships
    # and we can set innerjoin to true if the relationship is nonnullable
    # https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html#joined-eager-loading
    # one issue with selectinload is it will not work with nested relationships
    # that have compositie primary keys. this shows up on sql server
    # https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html#select-in-loading
    query = query.options(selectinload(column))

    # TODO: this nested select is untested and probably doesn't work we want to
    # use chained loading to specify futher levels
    # https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html#relationship-loading-with-loader-options
    if non_scalar_field_columns:
        for field_column in non_scalar_field_columns:
            field, column = field_column
            column_type = get_type_for_column(info, column)
            do_nested_select(info, column_type, query, field, column, model)

    return query


def create_all_type_resolver(type_: type):
    """create a resolver for all instances of a type. Supports various filters"""
    from api.strawberry_sqlalchemy.schema_generation import (
        create_non_scalar_comparison_expression,
        create_non_scalar_order_by_expression,
        create_non_scalar_select_columns_enum,
    )

    def all_type_resolver(
        self,
        info,
        where: t.Optional[create_non_scalar_comparison_expression(type_)] = None,
        limit: t.Optional[int] = None,
        offset: t.Optional[int] = None,
        orderBy: t.Optional[create_non_scalar_order_by_expression(type_)] = None,
        distinctOn: t.Optional[
            t.List[create_non_scalar_select_columns_enum(type_)]
        ] = None,
    ) -> t.List[type_]:

        # handle the case where we are querying a many attribute
        # in a one to many relationship
        # the many attribute uses an all_type_query resolver so that the user
        # can supply filters. but  strawberry.field.get_result tries to
        # load the nested attribute using the resolver.
        # because we are using eager loading we actually just want to access
        # the attribute on the parent using get_attr(model, python_name)
        # we don't want to generate a nested query
        # TODO: to check that we are not at the root we check that the prev
        # path is not None. Not sure if this is always true!
        if info.path.prev is not None:
            return getattr(self, info.python_name)

        model = get_model_for_type(info, type_)

        db = info.context["db"]

        selected_fields = [s for s in info.selected_fields[0].selections]

        (
            scalar_field_columns,
            non_scalar_field_columns,
        ) = get_selected_scalar_non_scalar_field_columns(info, type_, selected_fields)

        query = select(model)

        if non_scalar_field_columns:
            for field_column in non_scalar_field_columns:
                field, column = field_column
                column_type = get_type_for_column(info, column)
                query = do_nested_select(info, column_type, query, field, column, model)

        rows = db.exec(query).all()

        return rows

    return all_type_resolver

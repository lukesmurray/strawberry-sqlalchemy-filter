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


def get_selected_field_columns(info, type_, selected_fields, model=None):

    strawberry_fields = get_strawberry_fields_for_type(info, type_)
    model = get_model_for_type(info, type_) if model is None else model

    # TODO: this is a hack to fix the snack_case bug. we assume camel_case is
    # true for get_graphql_name
    name_map = {f.get_graphql_name(True): f.python_name for f in strawberry_fields}

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

    query = query.add_columns(column)
    query = query.options(selectinload(column))

    if non_scalar_field_columns:
        # TODO: this probably breaks because the columns come from the model
        # and not from the column used to perform the nested select
        for field_column in non_scalar_field_columns:
            field, column = field_column
            column_type = get_type_for_column(info, column)
            do_nested_select(info, column_type, query, field, column, model)

    return query


def create_all_type_query(type_: type):
    from api.strawberry_sqlalchemy.schema_generation import (
        create_non_scalar_comparison_expression,
        create_non_scalar_order_by_expression,
        create_non_scalar_select_columns_enum,
    )

    def all_type_query_implementation(
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
        model = get_model_for_type(info, type_)
        db = info.context["db"]

        selected_fields = [s for s in info.selected_fields[0].selections]
        # TODO: hack to fix snack_case bug. we assume camel_case is true for
        # get_graphql_name but we need the schema to actually find out.
        # currently no way to access schema in resolvers also not sure that
        # type_._type_definition is always going to exist

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

        # TODO: this is where we're stuck now. when we pass movies we get an error
        # since movies is a list and we expect a resolver.
        results = [type_ for r in rows]
        return results

    return all_type_query_implementation

# Goal

Autogenerate a graphql schema from sqlalchemy models.

## Example

This is the movies and directors schema from the [strawberry fastapi-sqlalchemy example](https://github.com/strawberry-graphql/examples/tree/main/fastapi-sqlalchemy).

```python
class Director(Base):
    __tablename__ = "directors"

    id: int = Column(Integer, primary_key=True, index=True, nullable=False)
    name: str = Column(String, unique=True, index=True, nullable=False)


class Movie(Base):
    __tablename__ = "movies"

    id: int = Column(Integer, primary_key=True, index=True, nullable=False)
    title: str = Column(String, unique=True, nullable=False)
    imdb_id: str = Column(String, unique=True, index=True, nullable=False)
    year: int = Column(Integer, nullable=False)
    image_url: str = Column(String, nullable=False)
    imdb_rating: float = Column(Float, nullable=False)
    imdb_rating_count: str = Column(String, nullable=False)

    director_id: int = Column(Integer, ForeignKey("directors.id"), nullable=False)
    director: Director = relationship("Director")
```

When we add this schema to hasura we get the following graphql schema ([Added at the bottom](https://gist.github.com/lukesmurray/b7e64c3849d50a82cf06861fe35692f7#generated-schema) for readability).
The schema is really long but it is a good example of where we could go in the long run.

## Roadmap

- [x] implement automatic schema generation from strawberry types
- [ ] implement automatic schema generation from sqlalchemy types
- [ ] implement where clause
  - [x] schema generation
  - [ ] sqlalchemy integration
- [ ] implement limit/offset clauses
  - [x] schema generation
  - [ ] sqlalchemy integration
- [ ] implement order by clauses
  - [x] schema generation
  - [ ] sqlalchemy integration
- [ ] implement distinct clauses
  - [x] schema generation
  - [ ] sqlalchemy integration
- [ ] implement nested single item queries from the many to the one side of a relationship
  - [x] schema generation
  - [ ] sqlalchemy integration
- [ ] implement nested array queries from the one to the many side of a relationship
  - [x] schema generation
  - [ ] sqlalchemy integration
- [ ] implement where clauses for nested array queries
  - [ ] schema generation
  - [ ] sqlalchemy integration
- [ ] implement limit/offset clauses for nested array queries
  - [ ] schema generation
  - [ ] sqlalchemy integration
- [ ] implement order by clauses for nested array queries
  - [ ] schema generation
  - [ ] sqlalchemy integration
- [ ] implement distinct clauses for nested array queries
  - [ ] schema generation
  - [ ] sqlalchemy integration
- [ ] implement automatic query generation from sqlalchemy models
  - [ ] schema generation
  - [ ] sqlalchemy integration

In the future...

- [ ] Implement a relay api for queries
- [ ] Implement mutations
- [ ] Support hiding fields
- [ ] Support derived fields
- [ ] Add support/documentation to avoid n+1 selects

## Summary of Hasura Automatic Query Generation

1. For every table we can create a query over that table which supports the following inputs. The fields are the columns in the table.

- [ ] distinct
- [ ] limit
- [ ] offset
- [ ] order by
- [ ] where

2. We can also fetch aggregates which use the previous inputs but have the following fields. These fields are nested and refer to the columns of the table when they are valid. So for example avg would only contain numeric columns from the table.

- [ ] avg
- [ ] count
- [ ] max
- [ ] min
- [ ] stddev
- [ ] sum
- [ ] var

3. We can fetch items by their primary key.

4. If there are relationships we can fetch those but it depends on the type of relation. If we are fetching a single item then the item can be accessed directly. If we are fetching multiple items then we would support nested fetches using both 1 and 4

## Generated Schema

<summary>Expand to see schema
<details>

```graphql
schema {
  query: query_root
  mutation: mutation_root
  subscription: subscription_root
}

"""
whether this query should be cached (Hasura Cloud only)
"""
directive @cached(
  """
  measured in seconds
  """
  ttl: Int! = 60

  """
  refresh the cache entry
  """
  refresh: Boolean! = false
) on QUERY

"""
Boolean expression to compare columns of type "Int". All fields are combined with logical 'AND'.
"""
input Int_comparison_exp {
  _eq: Int
  _gt: Int
  _gte: Int
  _in: [Int!]
  _is_null: Boolean
  _lt: Int
  _lte: Int
  _neq: Int
  _nin: [Int!]
}

"""
Boolean expression to compare columns of type "String". All fields are combined with logical 'AND'.
"""
input String_comparison_exp {
  _eq: String
  _gt: String
  _gte: String

  """
  does the column match the given case-insensitive pattern
  """
  _ilike: String
  _in: [String!]

  """
  does the column match the given POSIX regular expression, case insensitive
  """
  _iregex: String
  _is_null: Boolean

  """
  does the column match the given pattern
  """
  _like: String
  _lt: String
  _lte: String
  _neq: String

  """
  does the column NOT match the given case-insensitive pattern
  """
  _nilike: String
  _nin: [String!]

  """
  does the column NOT match the given POSIX regular expression, case insensitive
  """
  _niregex: String

  """
  does the column NOT match the given pattern
  """
  _nlike: String

  """
  does the column NOT match the given POSIX regular expression, case sensitive
  """
  _nregex: String

  """
  does the column NOT match the given SQL regular expression
  """
  _nsimilar: String

  """
  does the column match the given POSIX regular expression, case sensitive
  """
  _regex: String

  """
  does the column match the given SQL regular expression
  """
  _similar: String
}

"""
columns and relationships of "directors"
"""
type directors {
  id: Int!

  """
  An array relationship
  """
  movies(
    """
    distinct select on columns
    """
    distinct_on: [movies_select_column!]

    """
    limit the number of rows returned
    """
    limit: Int

    """
    skip the first n rows. Use only with order_by
    """
    offset: Int

    """
    sort the rows by one or more columns
    """
    order_by: [movies_order_by!]

    """
    filter the rows returned
    """
    where: movies_bool_exp
  ): [movies!]!

  """
  An aggregate relationship
  """
  movies_aggregate(
    """
    distinct select on columns
    """
    distinct_on: [movies_select_column!]

    """
    limit the number of rows returned
    """
    limit: Int

    """
    skip the first n rows. Use only with order_by
    """
    offset: Int

    """
    sort the rows by one or more columns
    """
    order_by: [movies_order_by!]

    """
    filter the rows returned
    """
    where: movies_bool_exp
  ): movies_aggregate!
  name: String!
}

"""
aggregated selection of "directors"
"""
type directors_aggregate {
  aggregate: directors_aggregate_fields
  nodes: [directors!]!
}

"""
aggregate fields of "directors"
"""
type directors_aggregate_fields {
  avg: directors_avg_fields
  count(columns: [directors_select_column!], distinct: Boolean): Int!
  max: directors_max_fields
  min: directors_min_fields
  stddev: directors_stddev_fields
  stddev_pop: directors_stddev_pop_fields
  stddev_samp: directors_stddev_samp_fields
  sum: directors_sum_fields
  var_pop: directors_var_pop_fields
  var_samp: directors_var_samp_fields
  variance: directors_variance_fields
}

"""
aggregate avg on columns
"""
type directors_avg_fields {
  id: Float
}

"""
Boolean expression to filter rows from the table "directors". All fields are combined with a logical 'AND'.
"""
input directors_bool_exp {
  _and: [directors_bool_exp!]
  _not: directors_bool_exp
  _or: [directors_bool_exp!]
  id: Int_comparison_exp
  movies: movies_bool_exp
  name: String_comparison_exp
}

"""
unique or primary key constraints on table "directors"
"""
enum directors_constraint {
  """
  unique or primary key constraint
  """
  directors_name_key

  """
  unique or primary key constraint
  """
  directors_pkey
}

"""
input type for incrementing numeric columns in table "directors"
"""
input directors_inc_input {
  id: Int
}

"""
input type for inserting data into table "directors"
"""
input directors_insert_input {
  id: Int
  movies: movies_arr_rel_insert_input
  name: String
}

"""
aggregate max on columns
"""
type directors_max_fields {
  id: Int
  name: String
}

"""
aggregate min on columns
"""
type directors_min_fields {
  id: Int
  name: String
}

"""
response of any mutation on the table "directors"
"""
type directors_mutation_response {
  """
  number of rows affected by the mutation
  """
  affected_rows: Int!

  """
  data from the rows affected by the mutation
  """
  returning: [directors!]!
}

"""
input type for inserting object relation for remote table "directors"
"""
input directors_obj_rel_insert_input {
  data: directors_insert_input!

  """
  on conflict condition
  """
  on_conflict: directors_on_conflict
}

"""
on conflict condition type for table "directors"
"""
input directors_on_conflict {
  constraint: directors_constraint!
  update_columns: [directors_update_column!]! = []
  where: directors_bool_exp
}

"""
Ordering options when selecting data from "directors".
"""
input directors_order_by {
  id: order_by
  movies_aggregate: movies_aggregate_order_by
  name: order_by
}

"""
primary key columns input for table: directors
"""
input directors_pk_columns_input {
  id: Int!
}

"""
select columns of table "directors"
"""
enum directors_select_column {
  """
  column name
  """
  id

  """
  column name
  """
  name
}

"""
input type for updating data in table "directors"
"""
input directors_set_input {
  id: Int
  name: String
}

"""
aggregate stddev on columns
"""
type directors_stddev_fields {
  id: Float
}

"""
aggregate stddev_pop on columns
"""
type directors_stddev_pop_fields {
  id: Float
}

"""
aggregate stddev_samp on columns
"""
type directors_stddev_samp_fields {
  id: Float
}

"""
aggregate sum on columns
"""
type directors_sum_fields {
  id: Int
}

"""
update columns of table "directors"
"""
enum directors_update_column {
  """
  column name
  """
  id

  """
  column name
  """
  name
}

"""
aggregate var_pop on columns
"""
type directors_var_pop_fields {
  id: Float
}

"""
aggregate var_samp on columns
"""
type directors_var_samp_fields {
  id: Float
}

"""
aggregate variance on columns
"""
type directors_variance_fields {
  id: Float
}

scalar float8

"""
Boolean expression to compare columns of type "float8". All fields are combined with logical 'AND'.
"""
input float8_comparison_exp {
  _eq: float8
  _gt: float8
  _gte: float8
  _in: [float8!]
  _is_null: Boolean
  _lt: float8
  _lte: float8
  _neq: float8
  _nin: [float8!]
}

"""
columns and relationships of "movies"
"""
type movies {
  """
  An object relationship
  """
  director: directors!
  director_id: Int!
  id: Int!
  image_url: String!
  imdb_id: String!
  imdb_rating: float8!
  imdb_rating_count: String!
  title: String!
  year: Int!
}

"""
aggregated selection of "movies"
"""
type movies_aggregate {
  aggregate: movies_aggregate_fields
  nodes: [movies!]!
}

"""
aggregate fields of "movies"
"""
type movies_aggregate_fields {
  avg: movies_avg_fields
  count(columns: [movies_select_column!], distinct: Boolean): Int!
  max: movies_max_fields
  min: movies_min_fields
  stddev: movies_stddev_fields
  stddev_pop: movies_stddev_pop_fields
  stddev_samp: movies_stddev_samp_fields
  sum: movies_sum_fields
  var_pop: movies_var_pop_fields
  var_samp: movies_var_samp_fields
  variance: movies_variance_fields
}

"""
order by aggregate values of table "movies"
"""
input movies_aggregate_order_by {
  avg: movies_avg_order_by
  count: order_by
  max: movies_max_order_by
  min: movies_min_order_by
  stddev: movies_stddev_order_by
  stddev_pop: movies_stddev_pop_order_by
  stddev_samp: movies_stddev_samp_order_by
  sum: movies_sum_order_by
  var_pop: movies_var_pop_order_by
  var_samp: movies_var_samp_order_by
  variance: movies_variance_order_by
}

"""
input type for inserting array relation for remote table "movies"
"""
input movies_arr_rel_insert_input {
  data: [movies_insert_input!]!

  """
  on conflict condition
  """
  on_conflict: movies_on_conflict
}

"""
aggregate avg on columns
"""
type movies_avg_fields {
  director_id: Float
  id: Float
  imdb_rating: Float
  year: Float
}

"""
order by avg() on columns of table "movies"
"""
input movies_avg_order_by {
  director_id: order_by
  id: order_by
  imdb_rating: order_by
  year: order_by
}

"""
Boolean expression to filter rows from the table "movies". All fields are combined with a logical 'AND'.
"""
input movies_bool_exp {
  _and: [movies_bool_exp!]
  _not: movies_bool_exp
  _or: [movies_bool_exp!]
  director: directors_bool_exp
  director_id: Int_comparison_exp
  id: Int_comparison_exp
  image_url: String_comparison_exp
  imdb_id: String_comparison_exp
  imdb_rating: float8_comparison_exp
  imdb_rating_count: String_comparison_exp
  title: String_comparison_exp
  year: Int_comparison_exp
}

"""
unique or primary key constraints on table "movies"
"""
enum movies_constraint {
  """
  unique or primary key constraint
  """
  movies_imdb_id_key

  """
  unique or primary key constraint
  """
  movies_pkey

  """
  unique or primary key constraint
  """
  movies_title_key
}

"""
input type for incrementing numeric columns in table "movies"
"""
input movies_inc_input {
  director_id: Int
  id: Int
  imdb_rating: float8
  year: Int
}

"""
input type for inserting data into table "movies"
"""
input movies_insert_input {
  director: directors_obj_rel_insert_input
  director_id: Int
  id: Int
  image_url: String
  imdb_id: String
  imdb_rating: float8
  imdb_rating_count: String
  title: String
  year: Int
}

"""
aggregate max on columns
"""
type movies_max_fields {
  director_id: Int
  id: Int
  image_url: String
  imdb_id: String
  imdb_rating: float8
  imdb_rating_count: String
  title: String
  year: Int
}

"""
order by max() on columns of table "movies"
"""
input movies_max_order_by {
  director_id: order_by
  id: order_by
  image_url: order_by
  imdb_id: order_by
  imdb_rating: order_by
  imdb_rating_count: order_by
  title: order_by
  year: order_by
}

"""
aggregate min on columns
"""
type movies_min_fields {
  director_id: Int
  id: Int
  image_url: String
  imdb_id: String
  imdb_rating: float8
  imdb_rating_count: String
  title: String
  year: Int
}

"""
order by min() on columns of table "movies"
"""
input movies_min_order_by {
  director_id: order_by
  id: order_by
  image_url: order_by
  imdb_id: order_by
  imdb_rating: order_by
  imdb_rating_count: order_by
  title: order_by
  year: order_by
}

"""
response of any mutation on the table "movies"
"""
type movies_mutation_response {
  """
  number of rows affected by the mutation
  """
  affected_rows: Int!

  """
  data from the rows affected by the mutation
  """
  returning: [movies!]!
}

"""
on conflict condition type for table "movies"
"""
input movies_on_conflict {
  constraint: movies_constraint!
  update_columns: [movies_update_column!]! = []
  where: movies_bool_exp
}

"""
Ordering options when selecting data from "movies".
"""
input movies_order_by {
  director: directors_order_by
  director_id: order_by
  id: order_by
  image_url: order_by
  imdb_id: order_by
  imdb_rating: order_by
  imdb_rating_count: order_by
  title: order_by
  year: order_by
}

"""
primary key columns input for table: movies
"""
input movies_pk_columns_input {
  id: Int!
}

"""
select columns of table "movies"
"""
enum movies_select_column {
  """
  column name
  """
  director_id

  """
  column name
  """
  id

  """
  column name
  """
  image_url

  """
  column name
  """
  imdb_id

  """
  column name
  """
  imdb_rating

  """
  column name
  """
  imdb_rating_count

  """
  column name
  """
  title

  """
  column name
  """
  year
}

"""
input type for updating data in table "movies"
"""
input movies_set_input {
  director_id: Int
  id: Int
  image_url: String
  imdb_id: String
  imdb_rating: float8
  imdb_rating_count: String
  title: String
  year: Int
}

"""
aggregate stddev on columns
"""
type movies_stddev_fields {
  director_id: Float
  id: Float
  imdb_rating: Float
  year: Float
}

"""
order by stddev() on columns of table "movies"
"""
input movies_stddev_order_by {
  director_id: order_by
  id: order_by
  imdb_rating: order_by
  year: order_by
}

"""
aggregate stddev_pop on columns
"""
type movies_stddev_pop_fields {
  director_id: Float
  id: Float
  imdb_rating: Float
  year: Float
}

"""
order by stddev_pop() on columns of table "movies"
"""
input movies_stddev_pop_order_by {
  director_id: order_by
  id: order_by
  imdb_rating: order_by
  year: order_by
}

"""
aggregate stddev_samp on columns
"""
type movies_stddev_samp_fields {
  director_id: Float
  id: Float
  imdb_rating: Float
  year: Float
}

"""
order by stddev_samp() on columns of table "movies"
"""
input movies_stddev_samp_order_by {
  director_id: order_by
  id: order_by
  imdb_rating: order_by
  year: order_by
}

"""
aggregate sum on columns
"""
type movies_sum_fields {
  director_id: Int
  id: Int
  imdb_rating: float8
  year: Int
}

"""
order by sum() on columns of table "movies"
"""
input movies_sum_order_by {
  director_id: order_by
  id: order_by
  imdb_rating: order_by
  year: order_by
}

"""
update columns of table "movies"
"""
enum movies_update_column {
  """
  column name
  """
  director_id

  """
  column name
  """
  id

  """
  column name
  """
  image_url

  """
  column name
  """
  imdb_id

  """
  column name
  """
  imdb_rating

  """
  column name
  """
  imdb_rating_count

  """
  column name
  """
  title

  """
  column name
  """
  year
}

"""
aggregate var_pop on columns
"""
type movies_var_pop_fields {
  director_id: Float
  id: Float
  imdb_rating: Float
  year: Float
}

"""
order by var_pop() on columns of table "movies"
"""
input movies_var_pop_order_by {
  director_id: order_by
  id: order_by
  imdb_rating: order_by
  year: order_by
}

"""
aggregate var_samp on columns
"""
type movies_var_samp_fields {
  director_id: Float
  id: Float
  imdb_rating: Float
  year: Float
}

"""
order by var_samp() on columns of table "movies"
"""
input movies_var_samp_order_by {
  director_id: order_by
  id: order_by
  imdb_rating: order_by
  year: order_by
}

"""
aggregate variance on columns
"""
type movies_variance_fields {
  director_id: Float
  id: Float
  imdb_rating: Float
  year: Float
}

"""
order by variance() on columns of table "movies"
"""
input movies_variance_order_by {
  director_id: order_by
  id: order_by
  imdb_rating: order_by
  year: order_by
}

"""
mutation root
"""
type mutation_root {
  """
  delete data from the table: "directors"
  """
  delete_directors(
    """
    filter the rows which have to be deleted
    """
    where: directors_bool_exp!
  ): directors_mutation_response

  """
  delete single row from the table: "directors"
  """
  delete_directors_by_pk(id: Int!): directors

  """
  delete data from the table: "movies"
  """
  delete_movies(
    """
    filter the rows which have to be deleted
    """
    where: movies_bool_exp!
  ): movies_mutation_response

  """
  delete single row from the table: "movies"
  """
  delete_movies_by_pk(id: Int!): movies

  """
  insert data into the table: "directors"
  """
  insert_directors(
    """
    the rows to be inserted
    """
    objects: [directors_insert_input!]!

    """
    on conflict condition
    """
    on_conflict: directors_on_conflict
  ): directors_mutation_response

  """
  insert a single row into the table: "directors"
  """
  insert_directors_one(
    """
    the row to be inserted
    """
    object: directors_insert_input!

    """
    on conflict condition
    """
    on_conflict: directors_on_conflict
  ): directors

  """
  insert data into the table: "movies"
  """
  insert_movies(
    """
    the rows to be inserted
    """
    objects: [movies_insert_input!]!

    """
    on conflict condition
    """
    on_conflict: movies_on_conflict
  ): movies_mutation_response

  """
  insert a single row into the table: "movies"
  """
  insert_movies_one(
    """
    the row to be inserted
    """
    object: movies_insert_input!

    """
    on conflict condition
    """
    on_conflict: movies_on_conflict
  ): movies

  """
  update data of the table: "directors"
  """
  update_directors(
    """
    increments the numeric columns with given value of the filtered values
    """
    _inc: directors_inc_input

    """
    sets the columns of the filtered rows to the given values
    """
    _set: directors_set_input

    """
    filter the rows which have to be updated
    """
    where: directors_bool_exp!
  ): directors_mutation_response

  """
  update single row of the table: "directors"
  """
  update_directors_by_pk(
    """
    increments the numeric columns with given value of the filtered values
    """
    _inc: directors_inc_input

    """
    sets the columns of the filtered rows to the given values
    """
    _set: directors_set_input
    pk_columns: directors_pk_columns_input!
  ): directors

  """
  update data of the table: "movies"
  """
  update_movies(
    """
    increments the numeric columns with given value of the filtered values
    """
    _inc: movies_inc_input

    """
    sets the columns of the filtered rows to the given values
    """
    _set: movies_set_input

    """
    filter the rows which have to be updated
    """
    where: movies_bool_exp!
  ): movies_mutation_response

  """
  update single row of the table: "movies"
  """
  update_movies_by_pk(
    """
    increments the numeric columns with given value of the filtered values
    """
    _inc: movies_inc_input

    """
    sets the columns of the filtered rows to the given values
    """
    _set: movies_set_input
    pk_columns: movies_pk_columns_input!
  ): movies
}

"""
column ordering options
"""
enum order_by {
  """
  in ascending order, nulls last
  """
  asc

  """
  in ascending order, nulls first
  """
  asc_nulls_first

  """
  in ascending order, nulls last
  """
  asc_nulls_last

  """
  in descending order, nulls first
  """
  desc

  """
  in descending order, nulls first
  """
  desc_nulls_first

  """
  in descending order, nulls last
  """
  desc_nulls_last
}

type query_root {
  """
  fetch data from the table: "directors"
  """
  directors(
    """
    distinct select on columns
    """
    distinct_on: [directors_select_column!]

    """
    limit the number of rows returned
    """
    limit: Int

    """
    skip the first n rows. Use only with order_by
    """
    offset: Int

    """
    sort the rows by one or more columns
    """
    order_by: [directors_order_by!]

    """
    filter the rows returned
    """
    where: directors_bool_exp
  ): [directors!]!

  """
  fetch aggregated fields from the table: "directors"
  """
  directors_aggregate(
    """
    distinct select on columns
    """
    distinct_on: [directors_select_column!]

    """
    limit the number of rows returned
    """
    limit: Int

    """
    skip the first n rows. Use only with order_by
    """
    offset: Int

    """
    sort the rows by one or more columns
    """
    order_by: [directors_order_by!]

    """
    filter the rows returned
    """
    where: directors_bool_exp
  ): directors_aggregate!

  """
  fetch data from the table: "directors" using primary key columns
  """
  directors_by_pk(id: Int!): directors

  """
  An array relationship
  """
  movies(
    """
    distinct select on columns
    """
    distinct_on: [movies_select_column!]

    """
    limit the number of rows returned
    """
    limit: Int

    """
    skip the first n rows. Use only with order_by
    """
    offset: Int

    """
    sort the rows by one or more columns
    """
    order_by: [movies_order_by!]

    """
    filter the rows returned
    """
    where: movies_bool_exp
  ): [movies!]!

  """
  An aggregate relationship
  """
  movies_aggregate(
    """
    distinct select on columns
    """
    distinct_on: [movies_select_column!]

    """
    limit the number of rows returned
    """
    limit: Int

    """
    skip the first n rows. Use only with order_by
    """
    offset: Int

    """
    sort the rows by one or more columns
    """
    order_by: [movies_order_by!]

    """
    filter the rows returned
    """
    where: movies_bool_exp
  ): movies_aggregate!

  """
  fetch data from the table: "movies" using primary key columns
  """
  movies_by_pk(id: Int!): movies
}

type subscription_root {
  """
  fetch data from the table: "directors"
  """
  directors(
    """
    distinct select on columns
    """
    distinct_on: [directors_select_column!]

    """
    limit the number of rows returned
    """
    limit: Int

    """
    skip the first n rows. Use only with order_by
    """
    offset: Int

    """
    sort the rows by one or more columns
    """
    order_by: [directors_order_by!]

    """
    filter the rows returned
    """
    where: directors_bool_exp
  ): [directors!]!

  """
  fetch aggregated fields from the table: "directors"
  """
  directors_aggregate(
    """
    distinct select on columns
    """
    distinct_on: [directors_select_column!]

    """
    limit the number of rows returned
    """
    limit: Int

    """
    skip the first n rows. Use only with order_by
    """
    offset: Int

    """
    sort the rows by one or more columns
    """
    order_by: [directors_order_by!]

    """
    filter the rows returned
    """
    where: directors_bool_exp
  ): directors_aggregate!

  """
  fetch data from the table: "directors" using primary key columns
  """
  directors_by_pk(id: Int!): directors

  """
  An array relationship
  """
  movies(
    """
    distinct select on columns
    """
    distinct_on: [movies_select_column!]

    """
    limit the number of rows returned
    """
    limit: Int

    """
    skip the first n rows. Use only with order_by
    """
    offset: Int

    """
    sort the rows by one or more columns
    """
    order_by: [movies_order_by!]

    """
    filter the rows returned
    """
    where: movies_bool_exp
  ): [movies!]!

  """
  An aggregate relationship
  """
  movies_aggregate(
    """
    distinct select on columns
    """
    distinct_on: [movies_select_column!]

    """
    limit the number of rows returned
    """
    limit: Int

    """
    skip the first n rows. Use only with order_by
    """
    offset: Int

    """
    sort the rows by one or more columns
    """
    order_by: [movies_order_by!]

    """
    filter the rows returned
    """
    where: movies_bool_exp
  ): movies_aggregate!

  """
  fetch data from the table: "movies" using primary key columns
  """
  movies_by_pk(id: Int!): movies
}
```

</details>
</summary>

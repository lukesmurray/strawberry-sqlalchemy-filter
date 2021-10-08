# FastAPI + SQLAlchemy

This examples shows you how to setup Strawberry with FastAPI and SQLAlchemy. It
setups a GraphQL API to fetch the top rated movies from IMDB (stored in a sqlite
DB).

## How to use

1. Install dependencies

Use [poetry](https://python-poetry.org/) to install dependencies:

```bash
poetry install
```

<!--alex ignore hooks-->

2. Install pre-commit hooks

```bash
poetry run pre-commit install
```

3. Run migrations

Run [alembic](https://alembic.sqlalchemy.org/en/latest/) to create the database
and populate it with movie data:

```bash
poetry run alembic upgrade head
```

4. Run the server

Run [uvicorn](https://www.uvicorn.org/) to run the server:

```bash
poetry run uvicorn main:app --reload
```

The GraphQL API should now be available at http://localhost:8000/graphql

## Common Commands

- start the application
  - `poetry run uvicorn main:app --reload`
- output the schema
- `poetry run strawberry export-schema main:schema`

## Example query

```graphql
query AllTopRatedMovies {
  topRatedMovies {
    id
    imageUrl
    imdbId
    imdbRating
    imdbRatingCount
    title
    year
    director {
      id
      name
    }
  }
}
```

## Types of Filters

1. Automatically Generated
<!--alex ignore simple-->
2. Simple
3. Join

## Automatically Generated

| key    | description           |
| :----- | :-------------------- |
| eq     | equal                 |
| ne     | not equal             |
| like   | like                  |
| iLike  | insensitive like      |
| isNull | is null               |
| in     | in                    |
| notIn  | not in                |
| lt     | less than             |
| lte    | less than or equal    |
| gt     | greater than          |
| gte    | greater than or equal |

## Related Work

- [Strawberry Pagination Discussion](https://github.com/strawberry-graphql/strawberry/issues/175#issuecomment-934200864)
- [Fast API SqlAlchemy Strawberry Example](https://github.com/strawberry-graphql/examples/tree/main/fastapi-sqlalchemy)
  - [Another Example](https://github.com/ThirVondukr/manga-backend)
- [Strawberry Integration with Sql Model](https://github.com/strawberry-graphql/strawberry/discussions/1183#discussioncomment-1249751)
- [graphene sqlalchemy filter](https://github.com/art1415926535/graphene-sqlalchemy-filter)

## Examples

```graphql
{
  allUsers(
    filters: {
      isActive: true
      or: [{ isAdmin: true }, { usernameIn: ["moderator", "cool guy"] }]
    }
  ) {
    edges {
      node {
        id
        username
      }
    }
  }
}
```

```graphql
{
  allUsers(filters: { isActive: true }) {
    edges {
      node {
        id
      }
    }
  }
  allGroups {
    edges {
      node {
        users(filters: { isActive: true }) {
          edges {
            node {
              id
            }
          }
        }
      }
    }
  }
}
```

from fastapi import FastAPI
from strawberry.asgi import GraphQL


def create_app():
    from api.strawberry_sqlalchemy.movie_schema_example import schema

    graphql_app = GraphQL(schema)
    app = FastAPI()
    app.mount("/graphql", graphql_app)
    return app


app = create_app()

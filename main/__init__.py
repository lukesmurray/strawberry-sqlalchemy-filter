from api.strawberry_sqlalchemy.auto_schema import schema
from fastapi import FastAPI
from strawberry.asgi import GraphQL

graphql_app = GraphQL(schema)

app = FastAPI()
app.mount("/graphql", graphql_app)

from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from .query import Query
from .mutation import Mutation


graphql_app = GraphQLRouter(schema=Schema(query=Query, mutation=Mutation))

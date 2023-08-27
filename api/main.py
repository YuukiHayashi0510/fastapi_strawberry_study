import typing as T
from fastapi import FastAPI, Request, Response
from fastapi.responses import ORJSONResponse
import time

from src.graphql import graphql_app

app = FastAPI()

app.include_router(graphql_app, prefix="/graphql")


# @app.on_event("startup")
# def configure():
#     """サーバー起動前に実行"""
#     Base.metadata.create_all(engine)


@app.get("/hello")
def hello():
    """テスト用"""
    return {"message": "hello world!"}

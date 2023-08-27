from datetime import datetime, timedelta
import strawberry
from strawberry.types import Info

from src.auth.hash import Hash
from src.auth.inputs import SignUpInput, SignInInput
from src.auth.types import Token
from src.auth.service import (
    AuthService,
    ACCESS_TOKEN_LIFETIME_HOURS,
    REFRESH_TOKEN_LIFETIME_HOURS,
)
from src.tasks.types import TaskType
from src.tasks.resolver import add_task, update_task, update_task_status, delete_task


@strawberry.type
class Mutation:
    # @strawberry.mutation
    # def login(self, info: Info) -> bool:
    #     token = do_login()
    #     info.context["response"].set_cookie(key="token", value=token)
    #     return True
    @strawberry.field
    def sign_up(self, info: Info, input: SignUpInput) -> Token:
        auth_service = AuthService()
        token = auth_service.sign_up(**input.__dict__)
        access_token = token["access_token"]
        refresh_token = token["refresh_token"]
        now = datetime.now()
        access_utc_time = (now + timedelta(hours=ACCESS_TOKEN_LIFETIME_HOURS)).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        refresh_utc_time = (
            now + timedelta(hours=REFRESH_TOKEN_LIFETIME_HOURS)
        ).strftime("%Y-%m-%dT%H:%M:%SZ")

        info.context["response"].set_cookie(
            key="access_token", value=access_token, expires=access_utc_time
        )
        info.context["response"].set_cookie(
            key="refresh_token", value=refresh_token, expires=refresh_utc_time
        )
        return token

    @strawberry.field
    def sign_in(self, info: Info, input: SignInInput) -> Token:
        auth_service = AuthService()
        token = auth_service.sign_in(**input.__dict__)
        now = datetime.now()
        access_utc_time = (now + timedelta(hours=ACCESS_TOKEN_LIFETIME_HOURS)).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        refresh_utc_time = (
            now + timedelta(hours=REFRESH_TOKEN_LIFETIME_HOURS)
        ).strftime("%Y-%m-%dT%H:%M:%SZ")

        info.context["response"].set_cookie(
            key="access_token", value=token["access_token"], expires=access_utc_time
        )
        info.context["response"].set_cookie(
            key="refresh_token", value=token["refresh_token"], expires=refresh_utc_time
        )
        return Token(
            access_token=token["access_token"],
            refresh_token=token["refresh_token"],
            token_type=token["token_type"],
        )

    add_task: TaskType = strawberry.field(resolver=add_task)
    update_task: TaskType = strawberry.field(resolver=update_task)
    update_task_status: TaskType = strawberry.field(resolver=update_task_status)
    delete_task: TaskType = strawberry.field(resolver=delete_task)

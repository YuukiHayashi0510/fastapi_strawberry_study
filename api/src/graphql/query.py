import strawberry

from src.tasks.types import TaskWithUserType
from src.tasks.resolver import get_task, get_task_list


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello!"

    task: TaskWithUserType = strawberry.field(resolver=get_task)
    tasks: list[TaskWithUserType] = strawberry.field(resolver=get_task_list)

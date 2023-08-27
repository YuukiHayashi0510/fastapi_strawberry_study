from typing import Optional
import strawberry

from .types import StatusType


@strawberry.input
class AddTaskInput:
    name: str
    description: Optional[str] = None

@strawberry.input
class UpdateTaskInput:
    id: int
    name: str
    description: Optional[str] = None
    status: StatusType

@strawberry.input
class UpdateTaskStatusInput:
    id: int
    status: StatusType

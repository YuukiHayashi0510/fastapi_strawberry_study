from datetime import datetime
from typing import Optional
import strawberry

from src.users.types import UserType
from models import TaskStatus

StatusType = strawberry.enum(TaskStatus, name="Status")


@strawberry.type
class TaskType:
    id: int
    name: str
    description: Optional[str]
    status: StatusType
    created_at: datetime
    updated_at: datetime
    user_id: int


@strawberry.type
class TaskWithUserType(TaskType):
    user: UserType

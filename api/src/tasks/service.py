from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status as HttpStatus

from models import Task, TaskStatus
from db import SessionService


class TaskService(SessionService):
    def create(self, *, name: str, description: Optional[str] = None) -> Task:
        task = Task(name, description)
        self.save(task)
        return task

    def update(
        self,
        *,
        id: int,
        name: str,
        description: Optional[str] = None,
        status: TaskStatus
    ) -> Task:
        task = self.find_by_id(id)
        if task is None:
            raise HTTPException(
                status_code=HttpStatus.HTTP_404_NOT_FOUND, detail="Task is not found."
            )

        task.name = name
        task.description = description
        task.status = status
        task.updated_at = datetime.now()
        self.save(task)

        return task

    def update_status(self, *, id: int, status: TaskStatus) -> Task:
        task = self.find_by_id(id)
        if task is None:
            raise HTTPException(
                status_code=HttpStatus.HTTP_404_NOT_FOUND, detail="Task is not found."
            )

        task.status = status
        task.updated_at = datetime.now()
        self.save(task)

        return task

    def delete(self, *, id: int) -> Task:
        task = self.find_by_id(id)
        if task is None:
            raise HTTPException(
                status_code=HttpStatus.HTTP_404_NOT_FOUND, detail="Task is not found."
            )

        self.session.delete(task)
        return task

    def find_all(self) -> List[Task]:
        return self.session.query(Task).options(joinedload(Task.user)).all()

    def find_by_id(self, id: int):
        return (
            self.session.query(Task)
            .where(Task.id == id)
            .options(joinedload(Task.user))
            .first()
        )

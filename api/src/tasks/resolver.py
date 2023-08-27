from .inputs import AddTaskInput, UpdateTaskStatusInput, UpdateTaskInput
from src.tasks.service import TaskService


def get_task(id: int):
    service = TaskService()
    return service.find_by_id(id)


def get_task_list():
    service = TaskService()
    return service.find_all()


def add_task(input: AddTaskInput):
    service = TaskService()
    return service.create(**input.__dict__)


def update_task(input: UpdateTaskInput):
    service = TaskService()
    return service.update(**input.__dict__)


def update_task_status(input: UpdateTaskStatusInput):
    service = TaskService()
    return service.update_status(**input.__dict__)


def delete_task(id: int):
    service = TaskService()
    return service.delete(id)

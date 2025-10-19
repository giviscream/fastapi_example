from functools import lru_cache
from typing import List

from fastapi import Depends
from models.todo_task import ToDoTask
from models.user import User
from repositories.todo_tasks_repository import (
    ToDoTaskRepository,
    get_todo_tasks_repository,
)
from repositories.users_repository import UsersRepository
from schemas.todo_task.request import CreateToDoTask
from schemas.todo_task.response import ToDoTaskResponse
from services.base import transactional


class ToDoTaskService:
    def __init__(
        self,
        todo_tasks_repository: ToDoTaskRepository,
    ):
        self.todo_tasks_repository = todo_tasks_repository

    @transactional(repository_attr="todo_tasks_repository")
    async def create_todo_task(
        self, responsible_id: int, todo_task_create: CreateToDoTask
    ) -> ToDoTaskResponse:
        # Проверка существования пользователя
        # user: User = await self.users_repository.get_by_id(responsible_id)
        # if not user:
        #     raise ValueError("User not found")

        new_todo_task: ToDoTask = await self.todo_tasks_repository.create(
            title=todo_task_create.title,
            description=todo_task_create.description,
            responsible_id=responsible_id
        )

        return ToDoTaskResponse.model_validate(new_todo_task)

    async def get_todo_task(self, task_id: int) -> ToDoTaskResponse:
        todo_task: ToDoTask = await self.todo_tasks_repository.get_by_id(task_id)
        if not todo_task:
            return None
        return ToDoTaskResponse.model_validate(todo_task)

    async def get_all_todo_tasks(
        self, skip: int = 0, limit: int = 100
    ) -> List[ToDoTaskResponse]:
        todo_tasks: List[ToDoTask] = await self.todo_tasks_repository.list(
            skip=skip, limit=limit
        )
        return [ToDoTaskResponse.model_validate(todo_task) for todo_task in todo_tasks]


def get_todo_task_service(
    todo_tasks_repository=Depends(get_todo_tasks_repository),
):
    return ToDoTaskService(
        todo_tasks_repository=todo_tasks_repository,
    )

from logging import Logger
from typing import List

from models.todo_task import ToDoTask
from repositories.todo_tasks_repository import ToDoTaskRepository
from schemas.todo_task.request import CreateToDoTask
from schemas.todo_task.response import ToDoTaskResponse
from services.base import transactional


class ToDoTaskService:
    def __init__(
        self,
        logger: Logger,
        todo_tasks_repository: ToDoTaskRepository,
    ):
        self.todo_tasks_repository = todo_tasks_repository
        self.logger = logger

    @transactional(repository_attr="todo_tasks_repository")
    async def create_todo_task(
        self, responsible_id: int, todo_task_create: CreateToDoTask
    ) -> ToDoTaskResponse:
        new_todo_task: ToDoTask = await self.todo_tasks_repository.create(
            title=todo_task_create.title,
            description=todo_task_create.description,
            responsible_id=responsible_id,
        )

        return ToDoTaskResponse.model_validate(obj=new_todo_task)

    async def get_todo_task(self, task_id: int) -> ToDoTaskResponse:
        todo_task: ToDoTask = await self.todo_tasks_repository.get_by_id(id=task_id)
        if not todo_task:
            return None
        return ToDoTaskResponse.model_validate(obj=todo_task)

    async def get_all_todo_tasks(
        self, skip: int = 0, limit: int = 100
    ) -> List[ToDoTaskResponse]:
        todo_tasks: List[ToDoTask] = await self.todo_tasks_repository.list(
            skip=skip, limit=limit
        )
        return [
            ToDoTaskResponse.model_validate(obj=todo_task) for todo_task in todo_tasks
        ]

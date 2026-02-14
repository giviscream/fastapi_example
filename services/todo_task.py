from logging import Logger
from typing import List
from uuid import UUID

from models.todo_task import ToDoTask
from repositories.todo_tasks_repository import ToDoTaskRepository
from schemas.todo_task.query_params import ToDoTaskListParams
from schemas.todo_task.request import CreateToDoTask
from schemas.todo_task.response import ToDoTaskResponse
from sqlalchemy.ext.asyncio import AsyncSession


class ToDoTaskService:
    def __init__(
        self,
        logger: Logger,
        todo_tasks_repository: ToDoTaskRepository,
        session: AsyncSession,
    ):
        self.todo_tasks_repository = todo_tasks_repository
        self.logger = logger
        self.session = session

    async def create_todo_task(
        self, responsible_id: int, todo_task_create: CreateToDoTask
    ) -> ToDoTaskResponse:
        new_todo_task: ToDoTask = await self.todo_tasks_repository.create(
            session=self.session,
            title=todo_task_create.title,
            description=todo_task_create.description,
            responsible_id=responsible_id,
        )

        return ToDoTaskResponse.model_validate(obj=new_todo_task)

    async def get_todo_task(self, task_id: int) -> ToDoTaskResponse:
        todo_task: ToDoTask = await self.todo_tasks_repository.get_by_id(id=task_id)
        return ToDoTaskResponse.model_validate(obj=todo_task)

    async def get_user_todo_task(self, user_id: UUID, task_id: int) -> ToDoTaskResponse:
        todo_task: ToDoTask = await self.todo_tasks_repository.get_one(
            session=self.session,
            id=task_id,
            responsible_id=user_id,
        )
        return ToDoTaskResponse.model_validate(obj=todo_task)

    async def get_user_all_todo_tasks(
        self,
        user_id: UUID,
        list_params: ToDoTaskListParams,
    ) -> List[ToDoTaskResponse]:
        todo_tasks: List[ToDoTask] = await self.todo_tasks_repository.list(
            session=self.session,
            responsible_id=user_id,
            limit=list_params.pagination.limit,
            offset=list_params.pagination.offset,
            sort_by=list_params.sorting.sort_by,
            sort_order=list_params.sorting.sort_order,
            date_from=list_params.dt_range_filter.date_from,
            date_to=list_params.dt_range_filter.date_to,
        )
        return [
            ToDoTaskResponse.model_validate(obj=todo_task) for todo_task in todo_tasks
        ]

from uuid import UUID

from sqlalchemy import select
from models.todo_task import ToDoTask
from repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class ToDoTaskRepository(BaseRepository[ToDoTask]):
    def __init__(
        self,
        session: AsyncSession | None = None,
    ):
        super().__init__(session=session, model=ToDoTask)

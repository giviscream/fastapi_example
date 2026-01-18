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

    async def get_user_todo_task(self, responsible_id: UUID, todo_task_id: UUID) -> ToDoTask | None:
        result = await self.session.execute(
            select(self.model).where(self.model.responsible_id == responsible_id, self.model.id == todo_task_id)
        )
        return result.scalar_one_or_none()
    
    async def list_user_todo_tasks(self, responsible_id: UUID,  skip: int = 0, limit: int = 100) -> list[ToDoTask]:
        result = await self.session.execute(
            select(self.model).where(self.model.responsible_id == responsible_id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
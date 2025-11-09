from models.todo_task import ToDoTask
from models.user import User
from repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class ToDoTaskRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=ToDoTask)

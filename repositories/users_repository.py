from sqlalchemy import select

from models.user import User
from repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UsersRepository(BaseRepository[User]):
    def __init__(
        self,
        session: AsyncSession | None = None,
    ):
        super().__init__(session=session, model=User)

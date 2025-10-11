from functools import lru_cache
from fastapi import Depends
from database.database import get_db_session
from models.user import User
from repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UsersRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=User)

@lru_cache
def get_users_repository(session: AsyncSession = Depends(get_db_session)):
    return UsersRepository(session=session)

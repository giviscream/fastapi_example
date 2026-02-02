from models.user import User
from repositories.base import BaseRepository


class UsersRepository(BaseRepository[User]):
    def __init__(
        self,
    ):
        super().__init__(model=User)

from repositories.users_repository import UsersRepository, get_users_repository
from schemas.user.request import CreateUser
from models.user import User
from schemas.user.response import UserResponse
from functools import lru_cache
from fastapi import Depends

from services.base import transactional #todo: Как лучше?


class UserService:
    def __init__(self, user_repository: UsersRepository) -> None:
        self.user_repository = user_repository

    @transactional("user_repository")
    async def create_user(self, user_create: CreateUser) -> UserResponse:
        new_user: User = await self.user_repository.create(**user_create.model_dump())
        
        return UserResponse.model_validate(new_user)
    
@lru_cache
def get_user_service(user_repository = Depends(get_users_repository)):
    return UserService(user_repository=user_repository)

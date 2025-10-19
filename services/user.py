from repositories.users_repository import UsersRepository, get_users_repository
from schemas.token.response import Token
from schemas.user.request import CreateUser
from models.user import User
from schemas.user.response import UserResponse
from functools import lru_cache
from fastapi import Depends

from services.security_service import SecurityService
from services.base import transactional  # todo: Как лучше?


class UserService:
    def __init__(self, user_repository: UsersRepository) -> None:
        self.user_repository = user_repository

    @transactional("user_repository")
    async def create_user(self, user_create: CreateUser) -> UserResponse:
        password_hash = SecurityService.hash_password(user_create.password)
        new_user: User = await self.user_repository.create(
            email=user_create.email,
            username=user_create.username,
            password_hash=password_hash
        )

        return UserResponse.model_validate(new_user)

    async def authenticate_user(self, email: str, password: str) -> User | None:
        user: User = await self.user_repository.get_by_email(email=email)
        if not user:
            return None
        if user.disabled:
            return None
        if not SecurityService.verify_password(password, user.password_hash):
            return None
        return user

    async def login(self, email: str, password: str) -> Token:
        """
        Вход пользователя и создание JWT токена
        username может быть email или username
        """
        user = await self.authenticate_user(email=email, password=password)
        if not user:
            raise ValueError("Incorrect username or password")

        access_token = SecurityService.create_access_token(
            data={"sub": str(user.id), "email": user.email, "username": user.username},
        )

        return Token(access_token=access_token, token_type="bearer")


def get_user_service(user_repository=Depends(get_users_repository)):
    return UserService(user_repository=user_repository)

from logging import Logger
from fastapi import Depends
from core.logger import get_logger
from schemas.user.request import CreateUser
from schemas.user.response import UserResponse
from services.base import transactional
from services.security import SecurityService, get_security_service
#from core.exceptions import UnauthorizedException, AlreadyExistsException
from repositories.users_repository import UsersRepository, get_users_repository
from schemas.token.response import Token
from models.user import User


class AuthService:
    def __init__(
        self,
        users_repository: UsersRepository,
        security_service: SecurityService,
        logger: Logger
    ) -> None:
        self.users_repository = users_repository
        self.security_service = security_service

    @transactional(repository_attr="user_repository")
    async def create_user(self, user_create: CreateUser) -> UserResponse:
        password_hash = self.security_service.hash_password(
            password=user_create.password
        )
        new_user: User = await self.users_repository.create(
            email=user_create.email,
            username=user_create.username,
            password_hash=password_hash,
        )

        return UserResponse.model_validate(new_user)

    async def authenticate_user(self, email: str, password: str) -> User | None:
        user: User = await self.users_repository.get_by_email(email=email)
        if not user:
            return None
        if user.disabled:
            return None
        if not self.security_service.verify_password(
            plain_password=password,
            hashed_password=user.password_hash,
        ):
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

        access_token = self.security_service.create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "username": user.username,
            },
        )

        return Token(access_token=access_token, token_type="bearer")

    async def get_current_user(self, token: str) -> User:
        """Получение текущего пользователя из токена"""
        payload: dict = self.security_service.decode_access_token(token=token)
        username = payload.get("username")
        if not username:
            raise "Cannot verify username" #todo: сделать выделенные исключения

        user: User | None = await self.users_repository.get_by_username(
            username=username
        )
        if user is None:
            raise "Пользователь не найден"

        if user.disabled:
            raise "Пользователь неактивен"

        return user


def get_auth_service(
    user_repository=Depends(get_users_repository),
    security_service=Depends(get_security_service),
    logger=Depends(get_logger),
):
    return AuthService(
        logger=logger,
        user_repository=user_repository,
        security_service=security_service,
    )

from logging import Logger
from uuid import UUID
from exceptions import UnauthorizedException, InvalidTokenException
from schemas.user.request import CreateUser
from schemas.user.response import UserResponse
from services.security import SecurityService

from repositories.users_repository import UsersRepository
from schemas.token.response import Token
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
    def __init__(
        self,
        users_repository: UsersRepository,
        security_service: SecurityService,
        logger: Logger,
        session: AsyncSession,
    ) -> None:
        self.users_repository = users_repository
        self.security_service = security_service
        self.logger = logger
        self.session = session

    async def _authenticate(self, username: str, password: str) -> User:
        user: User = await self.users_repository.get_one(
            session=self.session, username=username, disabled=False
        )

        if not self.security_service.verify_password(
            plain_password=password,
            hashed_password=user.password_hash,
        ):
            raise UnauthorizedException(message="Incorrect username or password")
        return user

    async def create_user(self, user_create: CreateUser) -> UserResponse:
        password_hash = self.security_service.hash_password(
            password=user_create.password
        )
        new_user: User = await self.users_repository.create(
            session=self.session,
            email=user_create.email,
            username=user_create.username,
            full_name=user_create.full_name,
            password_hash=password_hash,
            disabled=False,
        )

        return UserResponse.model_validate(new_user)

    async def login(self, username: str, password: str) -> Token:
        """
        Вход пользователя и создание JWT токена
        """
        user: User = await self._authenticate(username=username, password=password)

        access_token = self.security_service.create_access_token(
            data={
                "user_id": str(user.id),
            },
        )

        return Token(access_token=access_token, token_type="bearer")

    async def get_current_user(self, token: str) -> UserResponse:
        """
        Получение текущего пользователя из токена
        """
        payload: dict = self.security_service.decode_access_token(token=token)
        user_id: UUID = payload.get("user_id")
        if not user_id:
            raise InvalidTokenException()

        user: User = await self.users_repository.get_one(
            session=self.session, id=user_id, disabled=False
        )

        return UserResponse.model_validate(user)

    async def get_current_user_id(self, token: str) -> UUID:
        result: UserResponse = await self.get_current_user(token=token)
        return result.id

    async def get_user_by_id(self, user_id: UUID) -> UserResponse:
        user: User = await self.users_repository.get_by_id(
            session=self.session, id=user_id
        )
        return UserResponse.model_validate(user)

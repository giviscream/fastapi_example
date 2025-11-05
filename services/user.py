from logging import Logger
from core.logger import get_logger
from repositories.users_repository import UsersRepository, get_users_repository
from fastapi import Depends

from services.security import SecurityService, get_security_service


class UserService:
    def __init__(
        self,
        logger: Logger,
        user_repository: UsersRepository,
        security_service: SecurityService,
    ) -> None:
        self.user_repository = user_repository
        self.security_service = security_service
        self.logger = logger


def get_user_service(
    user_repository=Depends(get_users_repository),
    security_service=Depends(get_security_service),
    logger=Depends(get_logger),
):
    return UserService(
        logger=logger,
        user_repository=user_repository,
        security_service=security_service,
    )

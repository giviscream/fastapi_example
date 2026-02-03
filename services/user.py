from logging import Logger
from repositories.users_repository import UsersRepository
from services.security import SecurityService


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

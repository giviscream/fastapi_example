from dependency_injector import containers, providers
from core.logger import setup_logger, LOGS_FMT, LOGS_DATE_FMT
from core.settings import settings
from database.database import Database
from repositories.todo_tasks_repository import ToDoTaskRepository
from repositories.users_repository import UsersRepository
from services.auth import AuthService
from services.security import SecurityService
from services.todo_report import TodoReportService
from services.todo_task import ToDoTaskService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.v1.auth",
            "api.v1.todo_tasks",
            "middleware.auth_middleware",
            "middleware.db_session_middleware",
            "database.ext",
        ]
    )

    logger = providers.Singleton(
        provides=setup_logger,
        logs_level=settings.LOGS_LEVEL,
        logs_fmt=LOGS_FMT,
        logs_date_fmt=LOGS_DATE_FMT,
        logger_name="fastapi_app",
    )

    db = providers.Singleton(
        provides=Database,
        database_url=settings.async_database_url,
        echo=True,
    )  # todo: пробрасывать его вместо сессий

    users_repository = providers.Factory(
        provides=UsersRepository,
    )

    todo_tasks_repository = providers.Factory(
        provides=ToDoTaskRepository,
    )

    security_service = providers.Factory(
        provides=SecurityService,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        sign_algorithm=settings.ALGORITHM,
        secret_key=settings.SECRET_KEY,
    )

    auth_service = providers.Factory(
        provides=AuthService,
        users_repository=users_repository,
        security_service=security_service,
        logger=logger,
    )

    todo_task_service = providers.Factory(
        provides=ToDoTaskService,
        todo_tasks_repository=todo_tasks_repository,
        session=providers.Dependency(),
        logger=logger,
    )
    todo_report_service = providers.Factory(
        provides=TodoReportService,
    )

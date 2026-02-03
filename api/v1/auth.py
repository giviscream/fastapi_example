from typing import Callable
from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from core.containers import Container
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user_id, get_db_session
from database.ext import managed_db_session
from schemas.user.request import CreateUser
from schemas.user.response import UserResponse
from schemas.token.response import Token
from services.auth import AuthService
from dependency_injector.wiring import Provide, inject

router = APIRouter()


@router.get(
    path="/users/me",
    response_model=UserResponse,
)
@inject
@managed_db_session()
async def get_current_user_info(
    auth_service: Callable[..., AuthService] = Depends(
        Provide[Container.auth_service.provider]
    ),
    current_user_id: UUID = Depends(get_current_user_id),
    db_session: AsyncSession = Depends(get_db_session),
) -> UserResponse:
    return await auth_service(session=db_session).get_user_by_id(
        user_id=current_user_id
    )


@router.post(
    path="/",
    response_model=UserResponse,
)
@inject
@managed_db_session()
async def register(
    user_create: CreateUser,
    auth_service: Callable[..., AuthService] = Depends(
        Provide[Container.auth_service.provider]
    ),
    db_session: AsyncSession = Depends(get_db_session),
) -> UserResponse:
    """
    Регистрация нового пользователя (доступно без авторизации)
    """
    return await auth_service(session=db_session).create_user(user_create=user_create)


@router.post("/token", response_model=Token)
@inject
@managed_db_session()
async def login(
    auth_service: Callable[..., AuthService] = Depends(
        Provide[Container.auth_service.provider]
    ),
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: AsyncSession = Depends(get_db_session),
) -> Token:
    """
    OAuth2 совместимый endpoint для получения токена.
    Этот endpoint используется кнопкой "Authorize" в Swagger UI.

    Используется стандартная форма OAuth2:
    - **username**: username пользователя
    - **password**: Пароль пользователя

    Возвращает JWT access token
    """
    return await auth_service(session=db_session).login(
        username=form_data.username, password=form_data.password
    )

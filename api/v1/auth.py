from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from core.containers import Container
from core.dependencies import get_current_user
from schemas.user.request import CreateUser
from schemas.user.response import UserResponse
from schemas.token.response import Token
from services.auth import AuthService
from dependency_injector.wiring import Provide, inject

router = APIRouter()



@router.get("/users/me")
async def get_current_user_info(
    current_user: UserResponse = Depends(dependency=get_current_user),
) -> UserResponse:
    return current_user


@router.post(
    path="/",
    response_model=UserResponse,
)
@inject
async def register(
    user_create: CreateUser,
    auth_service: Annotated[AuthService, Depends(Provide[Container.auth_service])],
) -> UserResponse:
    """
    Регистрация нового пользователя (доступно без авторизации)
    """
    return await auth_service.create_user(user_create=user_create)


@router.post("/token", response_model=Token)
@inject
async def login(
    auth_service: Annotated[AuthService, Depends(Provide[Container.auth_service])],
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    OAuth2 совместимый endpoint для получения токена.
    Этот endpoint используется кнопкой "Authorize" в Swagger UI.

    Используется стандартная форма OAuth2:
    - **username**: username пользователя
    - **password**: Пароль пользователя

    Возвращает JWT access token
    """
    try:
        token = await auth_service.login(
            username=form_data.username, password=form_data.password
        )
        return token
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

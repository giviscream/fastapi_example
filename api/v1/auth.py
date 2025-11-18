from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from core.containers import Container

from core.dependencies import get_current_user_id
from schemas.user.request import CreateUser
from schemas.user.response import UserResponse
from schemas.token.response import Token
from services.auth import AuthService
from dependency_injector.wiring import Provide, inject

router = APIRouter()

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


@router.get(
    path="/users/me",
    response_model=UserResponse,
    dependencies=[Depends(oauth_scheme)]
)
@inject
async def get_current_user_info(
    current_user_id: UUID = Depends(get_current_user_id),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
) -> UserResponse:
    #return await auth_service.get_user_by_id(user_id=request.state.user_id)
    return await auth_service.get_user_by_id(user_id=current_user_id)


@router.post(
    path="/",
    response_model=UserResponse,
)
@inject
async def register(
    user_create: CreateUser,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
) -> UserResponse:
    """
    Регистрация нового пользователя (доступно без авторизации)
    """
    return await auth_service.create_user(user_create=user_create)


@router.post("/token", response_model=Token)
@inject
async def login(
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
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

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.user import User
from schemas.user.request import CreateUser
from schemas.user.response import UserResponse
from schemas.token.response import Token
from services.user import UserService, get_user_service

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")


@router.get(path="/me")
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = None
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


@router.post(
    path="/",
    response_model=UserResponse,
)
async def register(
    user_create: CreateUser,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    """
    Регистрация нового пользователя (доступно без авторизации)
    """
    return await user_service.create_user(user_create=user_create)


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
):
    """
    OAuth2 совместимый endpoint для получения токена.
    Этот endpoint используется кнопкой "Authorize" в Swagger UI.

    Используется стандартная форма OAuth2:
    - **username**: Email или username пользователя
    - **password**: Пароль пользователя

    Возвращает JWT access token
    """
    try:
        token = await user_service.login(
            email=form_data.username, password=form_data.password
        )
        return token
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

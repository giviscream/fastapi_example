from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.user.request import CreateUser
from schemas.user.response import UserResponse
from schemas.token.response import Token
from services.user import UserService, get_user_service

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")

@router.post(
    path="/",
    response_model=UserResponse,
)
async def register(
    user_create: CreateUser, user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """
    Регистрация нового пользователя (доступно без авторизации)
    """
    return await user_service.create_user(user_create=user_create)

@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service)
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
        token = await user_service.login(email=form_data.username, password=form_data.password)
        return token
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

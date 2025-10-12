from fastapi import APIRouter, Depends
from schemas.user.request import CreateUser
from schemas.user.response import UserResponse
from services.user import UserService, get_user_service

router = APIRouter()


@router.post(
    path="/",
    response_model=UserResponse,
)
async def create_user(
    user_create: CreateUser, user_service: UserService = Depends(get_user_service)
):
    """
    Регистрация нового пользователя (доступно без авторизации)
    """
    new_user: UserResponse = await user_service.create_user(user_create=user_create)
    return new_user

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import UUID

from exceptions.custom_exceptions.unauthorized import UnauthorizedException

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

def get_current_user_id(
    request: Request,
    _: str = Depends(oauth_scheme)
) -> UUID:
    """Dependency для получения текущего пользователя"""
    if not hasattr(request.state, "user_id"):
        raise UnauthorizedException()
    return request.state.user_id

def get_db_session(
        request: Request,
):
    return request.state.db_session


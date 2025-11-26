from fastapi import Depends, Request
from starlette.middleware.base import BaseHTTPMiddleware
from core.containers import Container
from database.database import Database
from dependency_injector.wiring import inject, Provide


class DBSessionMiddleware(BaseHTTPMiddleware):
    @inject
    async def dispatch(
        self,
        request: Request,
        call_next,
        db: Database = Depends(Provide[Container.db]),
    ):
        # Создаем сессию
        request.state.db_session = db.session_factory()
        try:
            response = await call_next(request)
            return response
        finally:
            if request.state.db_session:
                await request.state.db_session.close()

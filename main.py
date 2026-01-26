from fastapi import FastAPI
from contextlib import asynccontextmanager

import uvicorn
from api.v1 import todo_tasks, auth
from core.containers import Container
from middleware.auth_middleware import AuthMiddleware
from middleware.db_session_middleware import DBSessionMiddleware
from middleware.error_middleware import ErrorHandlingMiddleware

container = Container()
logger = container.logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("My fancy app is starting...")
    yield
    logger.info("My fancy app is done...")


def create_app(lifespan=lifespan) -> FastAPI:
    container = Container()
    app = FastAPI(lifespan=lifespan)
    app.container = container

    app.add_middleware(AuthMiddleware)
    app.add_middleware(DBSessionMiddleware)
    app.add_middleware(ErrorHandlingMiddleware, expose_internal_errors=False)

    app.include_router(
        router=auth.router,
        prefix="/api/v1/auth",
        tags=["Auth"],
    )
    app.include_router(
        router=todo_tasks.router,
        prefix="/api/v1/todo_tasks",
        tags=["ToDoTasks"],
    )

    return app


app = create_app(lifespan=lifespan)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

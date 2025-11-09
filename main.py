from fastapi import FastAPI
from contextlib import asynccontextmanager

import uvicorn
from api.v1 import todo_tasks, auth
from core.containers import Container

container = Container()
logger = container.logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("My fancy app is starting...")
    yield
    logger.info("My fancy app is done...")


def create_app(lifespan=lifespan) -> FastAPI:
    container = Container()

    # db = container.db()
    # db.create_database()

    app = FastAPI(lifespan=lifespan)
    app.container = container

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

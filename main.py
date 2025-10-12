from fastapi import FastAPI
from contextlib import asynccontextmanager

import uvicorn
#from database.database import init_db
from api.v1 import users, todo_tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    #init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(
    router=users.router,
    prefix="/api/v1/users",
    tags=["Users"],
)
app.include_router(
    router=todo_tasks.router,
    prefix="/api/v1/todo_tasks",
    tags=["ToDoTasks"],
)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
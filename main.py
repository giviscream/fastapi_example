from fastapi import FastAPI
from contextlib import asynccontextmanager
#from database.database import init_db
from api.v1 import users


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

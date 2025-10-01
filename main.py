from fastapi import FastAPI
from contextlib import asynccontextmanager
from core import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    lifespan=lifespan
)


@app.get("/")
async def get_root():
    return {"ok": True}

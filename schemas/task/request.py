from pydantic import BaseModel, Field


class CreateToDoRequest(BaseModel):
    title: str = Field(description="Заголовок задачи")
    
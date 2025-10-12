from pydantic import BaseModel, Field


class CreateToDoTask(BaseModel):
    title: str = Field(description="Заголовок задачи")
    description: str = Field(...)


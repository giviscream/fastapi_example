from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class ToDoTaskResponse(BaseModel):
    id: UUID = Field(...)
    title: str = Field(...)
    description: str = Field(...)
    responsible_id: UUID = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

    class Config:
        from_attributes = True
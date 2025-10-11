from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class UserResponse(BaseModel):

    id: UUID = Field(...)
    username: str = Field(...)
    email: str = Field(...)
    full_name: str | None = Field(...)
    disabled: bool = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

    class Config:
        from_attributes = True
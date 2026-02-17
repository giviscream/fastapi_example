from pydantic import BaseModel, Field

class CreateUser(BaseModel):
    username: str = Field(...)
    email: str | None = Field(...)
    full_name: str | None = Field(...)
    password: str = Field(...)
    
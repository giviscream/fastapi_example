from pydantic import BaseModel, Field

class CreateUser(BaseModel):
    username: str = Field(...)
    email: str = Field(...)
    full_name: str | None = Field(...)
    disabled: bool = Field(...)
    password_hash: str = Field(...)
    
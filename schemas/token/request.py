from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    email: str = Field(...)
    password: str = Field(...)
from typing import TypedDict

from pydantic import BaseModel, EmailStr, Field, field_validator


class User(TypedDict):
    id: int
    email: EmailStr
    username: str
    password: str


class CreateUserRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=4, max_length=32)
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        elif value in ("password", "pass1234"):
            raise ValueError("Password is too easy")
        return value


class UpdateUserRequest(BaseModel):
    email: EmailStr | None = None
    username: str | None = Field(default=None, min_length=4, max_length=32)
    password: str | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
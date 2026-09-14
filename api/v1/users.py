from typing import TypedDict

from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, EmailStr, Field, field_validator


class User(TypedDict):
    id: int
    email: EmailStr
    username: str
    password: str

users: list[User] = []


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


def find_user(user_id: int) -> User:
    for user in users:
        if user["id"] == user_id:
            return user

    raise HTTPException(status_code=404, detail="User not found")


router = APIRouter()

@router.post("/v1/users", status_code=201, response_model=UserResponse)
def create_user(user: CreateUserRequest) -> User:
    new_user: User = {
        "id": len(users) + 1,
        "email": user.email,
        "username": user.username,
        "password": user.password,
    }

    users.append(new_user)

    return new_user


@router.get("/v1/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int) -> User:
    return find_user(user_id)


@router.put("/v1/users/{user_id}", response_model=UserResponse)
def replace_user(user_id: int, data: CreateUserRequest) -> User:
    user = find_user(user_id)

    user["email"] = data.email
    user["username"] = data.username
    user["password"] = data.password

    return user


@router.patch("/v1/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: UpdateUserRequest) -> User:
    user = find_user(user_id)

    if data.email is not None:
        user["email"] = data.email

    if data.username is not None:
        user["username"] = data.username

    if data.password is not None:
        user["password"] = data.password

    return user


@router.delete("/v1/users/{user_id}", status_code=204)
def delete_user(user_id: int) -> Response:
    user = find_user(user_id)

    users.remove(user)

    return Response(status_code=204)
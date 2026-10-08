from fastapi import Depends, HTTPException
from pydantic import EmailStr

from repositories.users import UserRepository
from schemas import CreateUserRequest, UpdateUserRequest, User


class UserService:
    def __init__(self, repo: UserRepository = Depends()) -> None:
        self.repo = repo

    def create_user(self, raw_user: CreateUserRequest) -> User:
        if self.repo.get_user_by_email(raw_user.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        if self.repo.get_user_by_username(raw_user.username):
            raise HTTPException(status_code=400, detail="Username already registered")
        return self.repo.create_user(raw_user.username, raw_user.email, raw_user.password)

    def get_all_users(self) -> list[User]:
        return self.repo.get_all_users()

    def get_user_by_id(self, user_id: int) -> User:
        user = self.repo.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def replace_user(self, user_id: int, data: CreateUserRequest) -> User:
        self.get_user_by_id(user_id)
        self._validate_unique_fields(user_id, data.email, data.username)
        return self.repo.replace_user(user_id, data.username, data.email, data.password)

    def update_user(self, user_id: int, data: UpdateUserRequest) -> User:
        user = self.get_user_by_id(user_id)
        self._validate_unique_fields(
            user_id,
            data.email or user["email"],
            data.username or user["username"],
        )
        return self.repo.update_user(user_id, data.username, data.email, data.password)

    def delete_user(self, user_id: int) -> None:
        self.get_user_by_id(user_id)
        self.repo.delete_user(user_id)

    def _validate_unique_fields(self, user_id: int, email: EmailStr, username: str) -> None:
        email_user = self.repo.get_user_by_email(email)
        if email_user is not None and email_user["id"] != user_id:
            raise HTTPException(status_code=400, detail="Email already registered")
        username_user = self.repo.get_user_by_username(username)
        if username_user is not None and username_user["id"] != user_id:
            raise HTTPException(status_code=400, detail="Username already registered")

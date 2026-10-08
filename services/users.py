from fastapi import Depends, HTTPException

from models.users import UserModel
from repositories.users import UserRepository
from schemas import CreateUserRequest, UpdateUserRequest


class UserService:
    def __init__(self, repo: UserRepository = Depends()) -> None:
        self.repo = repo

    def create_user(self, raw_user: CreateUserRequest) -> UserModel:
        email = str(raw_user.email)
        if self.repo.get_user_by_email(email):
            raise HTTPException(status_code=400, detail="Email already registered")
        if self.repo.get_user_by_username(raw_user.username):
            raise HTTPException(status_code=400, detail="Username already registered")
        return self.repo.create_user(raw_user.username, email, raw_user.password)

    def get_all_users(self) -> list[UserModel]:
        return self.repo.get_all_users()

    def get_user_by_id(self, user_id: int) -> UserModel:
        user = self.repo.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def replace_user(self, user_id: int, data: CreateUserRequest) -> UserModel:
        user = self.get_user_by_id(user_id)
        email = str(data.email)
        self._validate_unique_fields(user_id, email, data.username)
        return self.repo.replace_user(user, data.username, email, data.password)

    def update_user(self, user_id: int, data: UpdateUserRequest) -> UserModel:
        user = self.get_user_by_id(user_id)
        email = str(data.email) if data.email is not None else user.email
        username = data.username if data.username is not None else user.username
        self._validate_unique_fields(user_id, email, username)
        return self.repo.update_user(user, data.username, data.email, data.password)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user_by_id(user_id)
        self.repo.delete_user(user)

    def _validate_unique_fields(self, user_id: int, email: str, username: str) -> None:
        email_user = self.repo.get_user_by_email(email)
        if email_user is not None and email_user.id != user_id:
            raise HTTPException(status_code=400, detail="Email already registered")
        username_user = self.repo.get_user_by_username(username)
        if username_user is not None and username_user.id != user_id:
            raise HTTPException(status_code=400, detail="Username already registered")

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.database import get_db
from models.users import UserModel


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get_user_by_email(self, email: str) -> UserModel | None:
        statement = select(UserModel).where(UserModel.email == email)
        return self.db.scalar(statement)

    def get_user_by_username(self, username: str) -> UserModel | None:
        statement = select(UserModel).where(UserModel.username == username)
        return self.db.scalar(statement)

    def create_user(self, username: str, email: str, password: str) -> UserModel:
        user = UserModel(username=username, email=email, password=password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_all_users(self) -> list[UserModel]:
        statement = select(UserModel).order_by(UserModel.id)
        return list(self.db.scalars(statement).all())

    def get_user_by_id(self, user_id: int) -> UserModel | None:
        return self.db.get(UserModel, user_id)

    def replace_user(
        self,
        user: UserModel,
        username: str,
        email: str,
        password: str,
    ) -> UserModel:
        user.username = username
        user.email = email
        user.password = password
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(
        self,
        user: UserModel,
        username: str | None,
        email: str | None,
        password: str | None,
    ) -> UserModel:
        if username is not None:
            user.username = username
        if email is not None:
            user.email = email
        if password is not None:
            user.password = password
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user: UserModel) -> None:
        self.db.delete(user)
        self.db.commit()

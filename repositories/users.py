from pydantic import EmailStr

from schemas import User


_users: dict[int, User] = {}


class UserRepository:
    def get_user_by_email(self, email: EmailStr) -> User | None:
        return next((user for user in _users.values() if user["email"] == email), None)

    def get_user_by_username(self, username: str) -> User | None:
        return next((user for user in _users.values() if user["username"] == username), None)

    def create_user(self, username: str, email: EmailStr, password: str) -> User:
        user_id = max(_users, default=0) + 1
        user: User = {
            "id": user_id,
            "username": username,
            "email": email,
            "password": password,
        }
        _users[user_id] = user
        return user

    def get_all_users(self) -> list[User]:
        return list(_users.values())

    def get_user_by_id(self, user_id: int) -> User | None:
        return _users.get(user_id)

    def replace_user(self, user_id: int, username: str, email: EmailStr, password: str) -> User:
        user = _users[user_id]
        user.update(username=username, email=email, password=password)
        return user

    def update_user(
        self,
        user_id: int,
        username: str | None,
        email: EmailStr | None,
        password: str | None,
    ) -> User:
        user = _users[user_id]
        if username is not None:
            user["username"] = username
        if email is not None:
            user["email"] = email
        if password is not None:
            user["password"] = password
        return user

    def delete_user(self, user_id: int) -> None:
        del _users[user_id]

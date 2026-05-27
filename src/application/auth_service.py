import hashlib
from domain import User, UserRepository
from domain.value_objects import Role
from typing import Optional


class AuthUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username, password) -> Optional[User]:
        user = self.user_repo.get_by_username(username)
        hashed_password = self._hash_password(password)
        if user and user.password == hashed_password:
            return user
        return None

    def create_user(self, username, password, role: str) -> None:
        hashed_password = self._hash_password(password)
        user = User(id=None, username=username, password=hashed_password, role=Role(role))
        self.user_repo.add_user(user)

    def update_user(self, username, password, role: str) -> None:
        hashed_password = self._hash_password(password)
        user = User(id=None, username=username, password=hashed_password, role=Role(role))
        self.user_repo.update_user(user)

    def get_all_users(self):
        return self.user_repo.get_all_users()

    def delete_user(self, username: str) -> None:
        self.user_repo.delete_user(username)

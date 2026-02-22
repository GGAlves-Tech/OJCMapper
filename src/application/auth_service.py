from domain import User, UserRepository
from typing import Optional

class AuthUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def login(self, username, password) -> Optional[User]:
        user = self.user_repo.get_by_username(username)
        if user and user.password == password:
            return user
        return None

    def create_user(self, username, password, role) -> None:
        user = User(id=None, username=username, password=password, role=role)
        self.user_repo.add_user(user)

    def update_user(self, username, password, role) -> None:
        user = User(id=None, username=username, password=password, role=role)
        self.user_repo.update_user(user)

    def delete_user(self, username: str) -> None:
        self.user_repo.delete_user(username)

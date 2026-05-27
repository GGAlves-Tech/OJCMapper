import hashlib
from typing import Optional
from domain import User, UserRepository
from domain.shared.value_objects import Role
from domain.shared.events import EventBus, UsuarioCriado, UsuarioRemovido


class AuthUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username: str, password: str) -> Optional[User]:
        user = self.user_repo.get_by_username(username)
        if user and user.password == self._hash_password(password):
            return user
        return None

    def get_all_users(self):
        return self.user_repo.get_all_users()

    def create_user(self, username: str, password: str, role: str) -> None:
        user = User(id=None, username=username, password=self._hash_password(password), role=Role(role))
        self.user_repo.add_user(user)
        EventBus.publish(UsuarioCriado(username=username, role=role))

    def update_user(self, username: str, password: str, role: str) -> None:
        user = User(id=None, username=username, password=self._hash_password(password), role=Role(role))
        self.user_repo.update_user(user)

    def delete_user(self, username: str) -> None:
        self.user_repo.delete_user(username)
        EventBus.publish(UsuarioRemovido(username=username))

import hashlib
import logging
from typing import Optional
from domain import User, UserRepository, Role, EventBus, UsuarioCriado, UsuarioRemovido
from domain.audit.audit_port import AuditPort

logger = logging.getLogger(__name__)


class AuthUseCase:
    def __init__(self, user_repo: UserRepository, audit: Optional[AuditPort] = None):
        self.user_repo = user_repo
        self.audit = audit

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username: str, password: str) -> Optional[User]:
        user = self.user_repo.get_by_username(username)
        if user and user.password == self._hash_password(password):
            return user
        return None

    def get_all_users(self):
        return self.user_repo.get_all_users()

    def create_user(self, username: str, password: str, role: str, actor: str = '') -> None:
        user = User(id=None, username=username, password=self._hash_password(password), role=Role(role))
        self.user_repo.add_user(user)
        EventBus.publish(UsuarioCriado(username=username, role=role))
        if self.audit:
            self.audit.log(actor, f'usuario-criado:{username}')

    def update_user(self, username: str, password: str, role: str, actor: str = '') -> None:
        user = User(id=None, username=username, password=self._hash_password(password), role=Role(role))
        self.user_repo.update_user(user)
        if self.audit:
            self.audit.log(actor, f'usuario-atualizado:{username}')

    def delete_user(self, username: str, actor: str = '') -> None:
        self.user_repo.delete_user(username)
        EventBus.publish(UsuarioRemovido(username=username))
        if self.audit:
            self.audit.log(actor, f'usuario-removido:{username}')

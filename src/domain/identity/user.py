from dataclasses import dataclass
from typing import Optional
from ..shared.role import Role


@dataclass
class User:
    id: Optional[int]
    username: str
    password: str
    role: Role

    def __post_init__(self):
        if not self.username or not self.username.strip():
            raise ValueError("username não pode ser vazio")
        if not isinstance(self.role, Role):
            raise TypeError(f"role deve ser Role, recebeu: {type(self.role).__name__}")

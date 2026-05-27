from abc import ABC, abstractmethod
from typing import List, Optional
from .user import User


class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass

    @abstractmethod
    def add_user(self, user: User) -> None:
        pass

    @abstractmethod
    def update_user(self, user: User) -> None:
        pass

    @abstractmethod
    def delete_user(self, username: str) -> None:
        pass

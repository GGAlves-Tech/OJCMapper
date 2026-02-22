from abc import ABC, abstractmethod
from typing import List, Optional
from .user import User
from .setting import Setting
from .project import Project

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

class SettingsRepository(ABC):
    @abstractmethod
    def get_all_settings(self) -> dict:
        pass

    @abstractmethod
    def update_setting(self, key: str, value: str) -> None:
        pass

class ProjectRepository(ABC):
    @abstractmethod
    def get_projects_by_type(self, project_type: str) -> List[Project]:
        pass

    @abstractmethod
    def delete_project(self, project_id: int) -> None:
        pass

from abc import ABC, abstractmethod
from typing import List
from .project import Project


class ProjectRepository(ABC):
    @abstractmethod
    def get_projects_by_type(self, project_type: str) -> List[Project]:
        pass

    @abstractmethod
    def delete_project(self, project_id: int) -> None:
        pass


class FileSystemPort(ABC):
    @abstractmethod
    def list_directories(self, path: str) -> list[str]:
        pass

    @abstractmethod
    def directory_exists(self, path: str) -> bool:
        pass

    @abstractmethod
    def delete_directory(self, path: str) -> None:
        pass

    @abstractmethod
    def move_directory(self, src: str, dst: str) -> None:
        pass

    @abstractmethod
    def write_text_file(self, path: str, content: str) -> None:
        pass

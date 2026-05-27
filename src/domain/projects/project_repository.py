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

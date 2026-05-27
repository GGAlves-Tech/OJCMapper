from dataclasses import dataclass
from typing import Optional
from ..shared.project_type import ProjectType


@dataclass
class Project:
    id: Optional[int]
    name: str
    type: ProjectType
    path: str

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("name não pode ser vazio")
        if not isinstance(self.type, ProjectType):
            raise TypeError(f"type deve ser ProjectType, recebeu: {type(self.type).__name__}")

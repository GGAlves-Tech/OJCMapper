import sqlite3
from domain import Project, ProjectType


class ProjectMapper:
    @staticmethod
    def to_domain(row: sqlite3.Row) -> Project:
        return Project(
            id=row['id'],
            name=row['name'],
            type=ProjectType(row['type']),
            path=row['path']
        )

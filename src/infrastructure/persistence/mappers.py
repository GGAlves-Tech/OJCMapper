from domain import User, Project, Setting
from domain.value_objects import Role, ProjectType
import sqlite3


class UserMapper:
    @staticmethod
    def to_domain(row: sqlite3.Row) -> User:
        return User(
            id=row['id'],
            username=row['username'],
            password=row['password'],
            role=Role(row['role'])
        )


class ProjectMapper:
    @staticmethod
    def to_domain(row: sqlite3.Row) -> Project:
        return Project(
            id=row['id'],
            name=row['name'],
            type=ProjectType(row['type']),
            path=row['path']
        )

class SettingMapper:
    @staticmethod
    def to_domain(row: sqlite3.Row) -> Setting:
        return Setting(
            id=row['id'],
            key=row['key'],
            value=row['value']
        )

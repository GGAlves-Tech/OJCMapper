from domain import User, Project, Setting
import sqlite3

class UserMapper:
    @staticmethod
    def to_domain(row: sqlite3.Row) -> User:
        return User(
            id=row['id'],
            username=row['username'],
            password=row['password'],
            role=row['role']
        )

class ProjectMapper:
    @staticmethod
    def to_domain(row: sqlite3.Row) -> Project:
        return Project(
            id=row['id'],
            name=row['name'],
            type=row['type'],
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

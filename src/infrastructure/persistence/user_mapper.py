import sqlite3
from domain import User, Role


class UserMapper:
    @staticmethod
    def to_domain(row: sqlite3.Row) -> User:
        return User(
            id=row['id'],
            username=row['username'],
            password=row['password'],
            role=Role(row['role'])
        )

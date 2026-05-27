import sqlite3
from domain import Setting


class SettingMapper:
    @staticmethod
    def to_domain(row: sqlite3.Row) -> Setting:
        return Setting(
            id=row['id'],
            key=row['key'],
            value=row['value']
        )

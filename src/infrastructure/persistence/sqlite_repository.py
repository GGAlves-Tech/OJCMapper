import sqlite3
from typing import List, Any, Optional
from domain.interfaces import BaseRepository

class SQLiteRepository(BaseRepository):
    """ Implementação genérica de repositório SQLite """
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """ Inicialização básica do banco de dados """
        conn = self._get_connection()
        # Aqui seriam criadas as tabelas base
        conn.commit()
        conn.close()

    def get_all(self) -> List[Any]:
        return []

    def get_by_id(self, id: Any) -> Optional[Any]:
        return None

    def add(self, entity: Any) -> None:
        pass

    def update(self, entity: Any) -> None:
        pass

    def delete(self, id: Any) -> None:
        pass

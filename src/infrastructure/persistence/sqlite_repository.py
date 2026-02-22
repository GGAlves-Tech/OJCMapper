from domain import User, Project, Setting, UserRepository, SettingsRepository, ProjectRepository
from .mappers import UserMapper, ProjectMapper, SettingMapper
from typing import List, Optional
import sqlite3

class SQLiteRepository(UserRepository, SettingsRepository, ProjectRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._get_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                path TEXT NOT NULL
            )
        ''')
        
        user_count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        if user_count == 0:
            conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', 
                         ('admin', 'admin', 'Gerente'))
            conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', 
                         ('editor', 'editor', 'Editor'))
            conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', 
                         ('user', 'user', 'Default'))
            
            settings = [
                ('online_path', '\\\\localhost\\Online'),
                ('gaveta_path', '\\\\localhost\\Gaveta'),
                ('av_medias_a_path', '\\\\localhost\\Media'),
                ('lista_path', '\\\\localhost\\Lists'),
                ('online_gaveta_status', 'OFFLINE'),
                ('log_path', './app.log'),
                ('sd_card_path', 'E:/'),
                ('remote_repo', '//server/repo'),
                ('network_user', 'guest'),
                ('network_password', 'password123')
            ]

            conn.executemany('INSERT INTO settings (key, value) VALUES (?, ?)', settings)
            
            projects = [
                ('Projeto A', 'ONLINE', 'Z:/Online/ProjetoA'),
                ('Projeto B', 'GAVETA', 'Y:/Gaveta/ProjetoB')
            ]
            conn.executemany('INSERT INTO projects (name, type, path) VALUES (?, ?, ?)', projects)
            
        conn.commit()
        conn.close()

    def get_by_username(self, username: str) -> Optional[User]:
        conn = self._get_connection()
        row = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        return UserMapper.to_domain(row) if row else None

    def get_all_users(self) -> List[User]:
        conn = self._get_connection()
        rows = conn.execute('SELECT * FROM users').fetchall()
        conn.close()
        return [UserMapper.to_domain(row) for row in rows]

    def add_user(self, user: User) -> None:
        conn = self._get_connection()
        conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', 
                     (user.username, user.password, user.role))
        conn.commit()
        conn.close()

    def update_user(self, user: User) -> None:
        conn = self._get_connection()
        conn.execute('UPDATE users SET password = ?, role = ? WHERE username = ?', 
                     (user.password, user.role, user.username))
        conn.commit()
        conn.close()

    def delete_user(self, username: str) -> None:
        conn = self._get_connection()
        conn.execute('DELETE FROM users WHERE username = ?', (username,))
        conn.commit()
        conn.close()

    def get_all_settings(self) -> dict:
        conn = self._get_connection()
        rows = conn.execute('SELECT key, value FROM settings').fetchall()
        conn.close()
        return {row['key']: row['value'] for row in rows}

    def update_setting(self, key: str, value: str) -> None:
        conn = self._get_connection()
        conn.execute('UPDATE settings SET value = ? WHERE key = ?', (value, key))
        conn.commit()
        conn.close()

    def get_projects_by_type(self, project_type: str) -> List[Project]:
        conn = self._get_connection()
        rows = conn.execute('SELECT * FROM projects WHERE type = ?', (project_type,)).fetchall()
        conn.close()
        return [ProjectMapper.to_domain(row) for row in rows]

    def delete_project(self, project_id: int) -> None:
        conn = self._get_connection()
        conn.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        conn.commit()
        conn.close()

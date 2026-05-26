-- OJCMapper — esquema SQLite
-- Espelha SQLiteRepository._init_db em sqlite_repository.py
--
-- Criar base vazia (exemplo):
--   sqlite3 ojcmapper.db < schema.sql
-- Apenas DDL: copie só os três blocos CREATE TABLE.

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    path TEXT NOT NULL
);

-- ---------------------------------------------------------------------------
-- Dados iniciais (a aplicação só insere isto quando a tabela users está vazia).
-- users/settings: INSERT OR IGNORE evita erro se voltar a correr. projects: sem UK
-- em name — não volte a executar os INSERT de projects na mesma base ou haverá duplicados.
-- ---------------------------------------------------------------------------

INSERT OR IGNORE INTO users (username, password, role) VALUES ('admin', 'admin', 'Gerente');
INSERT OR IGNORE INTO users (username, password, role) VALUES ('editor', 'editor', 'Editor');
INSERT OR IGNORE INTO users (username, password, role) VALUES ('user', 'user', 'Default');

INSERT OR IGNORE INTO settings (key, value) VALUES ('online_path', 'Z:/Online');
INSERT OR IGNORE INTO settings (key, value) VALUES ('gaveta_path', 'Y:/Gaveta');
INSERT OR IGNORE INTO settings (key, value) VALUES ('av_medias_a_path', 'X:/Media');
INSERT OR IGNORE INTO settings (key, value) VALUES ('lista_path', 'W:/Lists');
INSERT OR IGNORE INTO settings (key, value) VALUES ('online_gaveta_status', 'OFFLINE');
INSERT OR IGNORE INTO settings (key, value) VALUES ('log_path', './app.log');

INSERT INTO projects (name, type, path) VALUES ('Projeto A', 'ONLINE', 'Z:/Online/ProjetoA');
INSERT INTO projects (name, type, path) VALUES ('Projeto B', 'GAVETA', 'Y:/Gaveta/ProjetoB');

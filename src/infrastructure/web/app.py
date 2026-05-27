import logging
import secrets
import os
import sys
from flask import Flask
from application.auth_service import AuthUseCase
from application.project_service import ProjectUseCase
from application.map_service import MapUseCase
from application.delete_service import DeleteUseCase
from application.settings_service import SettingsUseCase
from application.export_service import ExportUseCase
from infrastructure.persistence.sqlite_repository import SQLiteRepository
from infrastructure.system.windows_mapper import WindowsDriveMapper
from infrastructure.system.filesystem_adapter import LocalFileSystemAdapter
from infrastructure.audit.file_audit_logger import FileAuditLogger

from .controllers.auth_controller import auth_bp
from .controllers.project_controller import project_bp
from .controllers.admin_controller import admin_bp


def _configure_logging() -> None:
    handler = logging.StreamHandler()
    handler.setLevel(logging.ERROR)
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    if not root.handlers:
        root.addHandler(handler)


def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_path, relative_path)


def create_app(db_path='database.db'):
    _configure_logging()

    template_dir = get_resource_path(os.path.join('infrastructure', 'web', 'templates'))
    static_dir = get_resource_path(os.path.join('infrastructure', 'web', 'static'))

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.secret_key = secrets.token_hex(16)

    if not os.path.isabs(db_path):
        if getattr(sys, 'frozen', False):
            db_path = os.path.join(os.path.dirname(sys.executable), db_path)
        else:
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), db_path)

    repo = SQLiteRepository(db_path)

    def _log_dir() -> str:
        raw = repo.get_all_settings().get('log_path', 'logs')
        if os.path.isabs(raw):
            return raw
        return os.path.join(os.path.dirname(os.path.abspath(db_path)), raw)

    audit = FileAuditLogger(log_dir_provider=_log_dir)
    drive_mapper = WindowsDriveMapper()
    fs = LocalFileSystemAdapter()

    app.auth_service = AuthUseCase(repo, audit=audit)
    app.project_service = ProjectUseCase(repo, repo, fs)
    app.map_service = MapUseCase(repo, drive_mapper, audit=audit)
    app.delete_service = DeleteUseCase(repo, fs, audit=audit)
    app.settings_service = SettingsUseCase(repo, audit=audit)
    app.export_service = ExportUseCase(repo, fs, audit=audit)

    app.register_blueprint(auth_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(admin_bp)

    return app

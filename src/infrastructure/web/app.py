import secrets
import os
import sys
from flask import Flask

# Domain & Application imports
from infrastructure.persistence.sqlite_repository import SQLiteRepository
from infrastructure.system.windows_mapper import WindowsDriveMapper
from application.auth_service import AuthUseCase
from application.project_service import ProjectUseCase
from application.map_service import MapUseCase
from application.delete_service import DeleteUseCase


# Web imports
from .controllers.home_controller import home_bp
from .controllers.admin_controller import admin_bp
from .controllers.auth_controller import auth_bp
from .controllers.project_controller import project_bp

def get_resource_path(relative_path):
    """ Returns absolute path to resource, compatible with PyInstaller """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        # File is at src/infrastructure/web/app.py
        # dirname(__file__) -> src/infrastructure/web
        # dirname(dirname(__file__)) -> src/infrastructure
        # dirname(dirname(dirname(__file__))) -> src/
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    return os.path.join(base_path, relative_path)

def create_app(db_path='database.db'):
    # Define paths for templates and static files relative to src/
    template_dir = get_resource_path(os.path.join('infrastructure', 'web', 'templates'))
    static_dir = get_resource_path(os.path.join('infrastructure', 'web', 'static'))
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    # Stable secret key for development to avoid logouts on reload
    if getattr(sys, 'frozen', False):
        app.secret_key = secrets.token_hex(16)
    else:
        app.secret_key = 'dev-secret-key-stable'
    
    # Register blueprints

    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(project_bp)
    
    # Inject services
    repo = SQLiteRepository(db_path)
    mapper = WindowsDriveMapper()
    
    app.auth_service = AuthUseCase(repo)
    app.project_service = ProjectUseCase(repo, repo)
    app.map_service = MapUseCase(repo, mapper)
    app.delete_service = DeleteUseCase(repo)
    app.repo = repo
    app.mapper = mapper
    
    return app


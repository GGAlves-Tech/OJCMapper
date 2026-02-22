import secrets
import os
import sys
from flask import Flask
from application.auth_service import AuthUseCase
from application.project_service import ProjectUseCase
from application.map_service import MapUseCase
from application.delete_service import DeleteUseCase
from infrastructure.persistence.sqlite_repository import SQLiteRepository
from infrastructure.system.windows_mapper import WindowsDriveMapper

from .controllers.auth_controller import auth_bp
from .controllers.project_controller import project_bp
from .controllers.admin_controller import admin_bp

def get_resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, compatível com PyInstaller """
    if getattr(sys, 'frozen', False):
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    else:
        # File is at src/infrastructure/web/app.py
        # dirname(dirname(dirname(__file__))) reaches src/
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    
    return os.path.join(base_path, relative_path)

def create_app(db_path='database.db'):
    # Define os caminhos de templates e estáticos
    template_dir = get_resource_path(os.path.join('infrastructure', 'web', 'templates'))
    static_dir = get_resource_path(os.path.join('infrastructure', 'web', 'static'))
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.secret_key = secrets.token_hex(16)
    
    # Resolve o caminho do banco de dados (se for relativo, coloca junto ao executável ou src)
    if not os.path.isabs(db_path):
        if getattr(sys, 'frozen', False):
            # No executável, o DB deve ficar na pasta do .exe, não na temporária _MEIPASS
            db_path = os.path.join(os.path.dirname(sys.executable), db_path)
        else:
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), db_path)

    repo = SQLiteRepository(db_path)
    mapper = WindowsDriveMapper()
    
    app.auth_service = AuthUseCase(repo)
    app.project_service = ProjectUseCase(repo, repo)
    app.map_service = MapUseCase(repo, mapper)
    app.delete_service = DeleteUseCase(repo)
    app.repo = repo
    app.mapper = mapper
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(admin_bp)
    
    return app

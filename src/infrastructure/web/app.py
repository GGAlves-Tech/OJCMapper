import secrets
import os
import sys
from flask import Flask
from .controllers.home_controller import home_bp

def get_resource_path(relative_path):
    """ Returns absolute path to resource, compatible with PyInstaller """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        # Base path is src/
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, relative_path)

def create_app():
    # Define paths for templates and static files relative to src/
    template_dir = get_resource_path(os.path.join('infrastructure', 'web', 'templates'))
    static_dir = get_resource_path(os.path.join('infrastructure', 'web', 'static'))
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.secret_key = secrets.token_hex(16)
    
    # Register basic routes
    app.register_blueprint(home_bp)
    
    return app

import webview
import threading
import sys
import os
import ctypes

# Ajusta o path para encontrar o src (Hexagonal)
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from infrastructure.web.app import create_app

def get_resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, compatível com PyInstaller """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
    return os.path.join(base_path, relative_path)

# Melhora a exibição do ícone na barra de tarefas do Windows
try:
    myappid = 'unitins.ojcmapper.v2'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

def start_flask():
    app = create_app()
    app.run(port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    # Inicia o Flask em uma thread separada
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    # Define o ícone
    icon_path = get_resource_path(os.path.join('infrastructure', 'web', 'static', 'app_icon.png'))

    # Cria a janela desktop nativa
    webview.create_window(
        'MAPPER OJC - Gestão de Projetos', 
        'http://127.0.0.1:5000',
        width=500,
        height=800,
        min_size=(500, 800),
        resizable=False,
        fullscreen=False,
        frameless=False,
        x=0,
        y=0
    )
    webview.start()

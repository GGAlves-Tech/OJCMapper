import webview
import threading
import sys
import os

# Ajusta o path para encontrar o src (Hexagonal)
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from infrastructure.web.app import create_app

def start_flask():
    app = create_app()
    app.run(port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    # Inicia o Flask em uma thread separada
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

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

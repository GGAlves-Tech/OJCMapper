import webview
import threading
import sys
import os

# Adds src to path (Hexagonal Architecture)
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from infrastructure.web.app import create_app

def start_flask():
    app = create_app()
    # Runs Flask in a specific port, no reloader to avoid issues with pywebview
    app.run(port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    # Start Flask in a background daemon thread
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    # Create the native desktop window pointing to the local Flask server
    webview.create_window(
        'Base Architecture - App', 
        'http://127.0.0.1:5000',
        width=1000,
        height=800,
        resizable=True
    )
    webview.start()

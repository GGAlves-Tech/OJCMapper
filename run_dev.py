import sys
import os

# Ajusta o path para encontrar o src (Hexagonal)
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from infrastructure.web.app import create_app

if __name__ == "__main__":
    # Script otimizado para desenvolvimento WEB
    # - debug=True: Ativa o auto-reload ao salvar arquivos
    # - Acessível via navegador (Chrome, Edge, etc.)
    app = create_app()
    print("\n🚀 Rodando em modo DESENVOLVIMENTO")
    print("👉 Acesse no seu navegador: http://127.0.0.1:5000\n")
    app.run(port=5000, debug=True)

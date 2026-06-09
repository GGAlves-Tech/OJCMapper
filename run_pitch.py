import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from infrastructure.web.app import create_app

if __name__ == '__main__':
    db = os.path.join(os.path.dirname(__file__), 'database_pitch.db')
    if not os.path.exists(db):
        print('\n[!] Banco de pitch nao encontrado. Execute primeiro:')
        print('    python scripts/setup_pitch_env.py\n')
        sys.exit(1)

    app = create_app(db_path=db)
    print('\nOJCMapper - modo PITCH (NAS simulado)')
    print('Navegador: http://127.0.0.1:5000')
    print('Login: admin / admin\n')
    app.run(port=5000, debug=True)

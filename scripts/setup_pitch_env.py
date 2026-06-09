"""Prepara pastas do NAS simulado e banco de dados para demo/pitch."""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAS = ROOT / 'nas-sim'

ONLINE_PROJECTS = [
    'Jornal_Tarde_08JUN',
    'VT_Reporter_Campo',
    'Entrevista_Governador_TO',
    'Materia_Policial_Palmas',
    'Esporte_No_Ar',
]

GAVETA_PROJECTS = [
    'Arquivo_2025_Marco',
    'CEDOC_Eleicoes_2024',
    'Jornal_Manha_Arquivado',
    'Especial_FestasJuninas_2023',
]

PLACEHOLDER = (
    '# Placeholder — simula pasta de projeto no Storage Quantum (NAS)\n'
    '# TV Anhanguera Palmas — ambiente de demonstração OJCMapper\n'
)


def _create_project_dirs(base: Path, names: list[str]) -> None:
    for name in names:
        folder = base / name
        folder.mkdir(parents=True, exist_ok=True)
        marker = folder / 'README.txt'
        if not marker.exists():
            marker.write_text(PLACEHOLDER + f'Projeto: {name}\n', encoding='utf-8')


def _ensure_nas_tree() -> None:
    _create_project_dirs(NAS / 'Online', ONLINE_PROJECTS)
    _create_project_dirs(NAS / 'Gaveta', GAVETA_PROJECTS)
    _create_project_dirs(NAS / 'Media', ONLINE_PROJECTS)
    (NAS / 'Lists').mkdir(parents=True, exist_ok=True)
    (NAS / 'Lists' / '.gitkeep').touch(exist_ok=True)


def _configure_database() -> Path:
    sys.path.insert(0, str(ROOT / 'src'))

    from infrastructure.persistence.sqlite_repository import SQLiteRepository

    db_path = ROOT / 'database_pitch.db'
    if db_path.exists():
        db_path.unlink()

    repo = SQLiteRepository(str(db_path))

    settings = {
        'online_path': str(NAS / 'Online'),
        'gaveta_path': str(NAS / 'Gaveta'),
        'av_medias_a_path': str(NAS / 'Media'),
        'lista_path': str(NAS / 'Lists'),
        'online_gaveta_status': 'ONLINE',
        'log_path': str(ROOT / 'logs_pitch'),
    }
    for key, value in settings.items():
        repo.update_setting(key, value)

    return db_path


def main() -> None:
    _ensure_nas_tree()
    db_path = _configure_database()
    logs_dir = ROOT / 'logs_pitch'
    logs_dir.mkdir(exist_ok=True)

    print('\n=== Ambiente de pitch configurado ===\n')
    print(f'NAS simulado : {NAS}')
    print(f'  Online     : {len(ONLINE_PROJECTS)} projetos')
    print(f'  Gaveta     : {len(GAVETA_PROJECTS)} projetos')
    print(f'  Media      : {len(ONLINE_PROJECTS)} pastas (mapeamento)')
    print(f'Banco        : {db_path}')
    print(f'Logs         : {logs_dir}')
    print('\nCredenciais de teste:')
    print('  admin / admin   (Gerente)')
    print('  editor / editor (Editor)')
    print('  user / user     (Default)')
    print('\nIniciar app real : python run_pitch.py')
    print('Protótipo Vite   : cd pitch-prototype && npm run dev\n')


if __name__ == '__main__':
    main()

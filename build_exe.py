import PyInstaller.__main__
import os
import shutil

# Nome do executável final
EXE_NAME = "MAPPER_OJC"

# Obter o diretório atual
base_dir = os.path.abspath(os.path.dirname(__file__))

# Limpar pastas de build anteriores
for folder in ['build', 'dist']:
    path = os.path.join(base_dir, folder)
    if os.path.exists(path):
        shutil.rmtree(path)

# Definir os arquivos de dados (templates, static, database)
# Formato: ('caminho_origem', 'caminho_destino_no_exe')
data_files = [
    (os.path.join('src', 'infrastructure', 'web', 'templates'), os.path.join('infrastructure', 'web', 'templates')),
    (os.path.join('src', 'infrastructure', 'web', 'static'), os.path.join('infrastructure', 'web', 'static')),
    ('database.db', '.'),
]

# Construir os argumentos do PyInstaller
params = [
    'main_desktop.py',           # Script principal
    '--name', EXE_NAME,          # Nome do .exe
    '--onefile',                 # Gerar apenas um arquivo
    '--noconsole',               # Não abrir console ao rodar
    '--paths', 'src',            # Adicionar a pasta src ao path de busca de módulos
    '--clean',                   # Limpar cache do PyInstaller antes de rodar
]

# Adicionar os data files como argumentos do PyInstaller
for src, dest in data_files:
    if os.path.exists(os.path.join(base_dir, src)):
        params.extend(['--add-data', f'{src}{os.pathsep}{dest}'])

print(f"Iniciando build de {EXE_NAME}...")
PyInstaller.__main__.run(params)

print(f"\nBuild concluído! O executável está em: {os.path.join(base_dir, 'dist', EXE_NAME + '.exe')}")

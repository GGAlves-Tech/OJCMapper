import os
from datetime import datetime
from domain import SettingsRepository
from domain.interfaces import FileSystemPort


class ExportUseCase:
    def __init__(self, settings_repo: SettingsRepository, fs: FileSystemPort):
        self.settings_repo = settings_repo
        self.fs = fs

    def export_media_list(self) -> dict:
        settings = self.settings_repo.get_all_settings()
        av_path = settings.get('av_medias_a_path', '').strip()
        lista_path = settings.get('lista_path', '').strip()

        if not av_path or not self.fs.directory_exists(av_path):
            return {'success': False, 'message': f'Caminho av_medias_a_path não configurado ou inválido: "{av_path}"'}

        if not lista_path or not self.fs.directory_exists(lista_path):
            return {'success': False, 'message': f'Caminho de Listas (lista_path) não configurado ou inválido: "{lista_path}"'}

        items = sorted(self.fs.list_directories(av_path))

        date_str = datetime.now().strftime('%d-%m-%y')
        filename = f'lista_delete_{date_str}.txt'
        output_path = os.path.join(lista_path, filename)

        content = f'Lista de projetos em: {av_path}\n'
        content += f'Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n'
        content += f'Total: {len(items)} projeto(s)\n'
        content += '-' * 60 + '\n'
        content += '\n'.join(items) + '\n'

        try:
            self.fs.write_text_file(output_path, content)
        except Exception as e:
            return {'success': False, 'message': f'Erro ao gravar arquivo: {e}'}

        return {'success': True, 'message': f'{len(items)} projeto(s) exportado(s) → {filename}'}

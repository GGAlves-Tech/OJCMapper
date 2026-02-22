import os
import shutil
from domain import SettingsRepository

class DeleteUseCase:
    def __init__(self, settings_repo: SettingsRepository):
        self.settings_repo = settings_repo

    def delete_projects(self, project_names: list[str], scope: str) -> dict:
        """
        Remove permanentemente a pasta do projeto em online_path ou gaveta_path
        (metadados) E a pasta correspondente em av_medias_a_path (mídias físicas).
        """
        settings = self.settings_repo.get_all_settings()
        
        path_key = 'online_path' if scope == 'ONLINE' else 'gaveta_path'
        metadata_base = settings.get(path_key, '').strip()
        av_medias_base = settings.get('av_medias_a_path', '').strip()

        done = []
        failed = []

        for name in project_names:
            try:
                # 1. Deleta Metadados
                if metadata_base:
                    meta_path = os.path.join(metadata_base, name)
                    if os.path.exists(meta_path):
                        shutil.rmtree(meta_path)
                
                # 2. Deleta Mídias
                if av_medias_base:
                    media_path = os.path.join(av_medias_base, name)
                    if os.path.exists(media_path):
                        shutil.rmtree(media_path)
                
                done.append(name)
            except Exception as e:
                failed.append({'name': name, 'error': str(e)})

        return {
            'success': len(failed) == 0,
            'message': f'{len(done)} projeto(s) removidos.' if not failed else f'Removidos {len(done)}, falha em {len(failed)}.',
            'done': done,
            'failed': failed
        }

    def engavetar_projects(self, project_names: list[str]) -> dict:
        """
        Move a PASTA INTEIRA do projeto de online_path para gaveta_path.
        A pasta deixa de existir no ONLINE e passa a existir na GAVETA.
        """
        settings = self.settings_repo.get_all_settings()
        online_base = settings.get('online_path', '').strip()
        gaveta_base = settings.get('gaveta_path', '').strip()

        if not online_base or not os.path.isdir(online_base):
            return {'success': False, 'message': 'Caminho ONLINE inválido.'}
        if not gaveta_base or not os.path.isdir(gaveta_base):
            return {'success': False, 'message': 'Caminho GAVETA inválido.'}

        done = []
        failed = []

        for name in project_names:
            src = os.path.join(online_base, name)
            dst = os.path.join(gaveta_base, name)
            try:
                if os.path.exists(src):
                    # Se já existir na gaveta, shutil.move pode falhar ou sobrescrever 
                    # dependendo da lógica do SO. Vamos remover o destino se existir 
                    # para garantir o move limpo.
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    
                    shutil.move(src, dst)
                    done.append(name)
                else:
                    failed.append({'name': name, 'error': 'Pasta não encontrada na origem.'})
            except Exception as e:
                failed.append({'name': name, 'error': str(e)})

        return {
            'success': len(failed) == 0,
            'message': f'{len(done)} projeto(s) engavetados.' if not failed else f'Engavetados {len(done)}, falha em {len(failed)}.',
            'done': done,
            'failed': failed
        }

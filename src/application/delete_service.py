import logging
import os
from typing import Optional
from domain import SettingsRepository, FileSystemPort, ProjectType, EventBus, ProjetoDeletado, ProjetoEngavetado
from domain.audit.audit_port import AuditPort

logger = logging.getLogger(__name__)


class DeleteUseCase:
    def __init__(self, settings_repo: SettingsRepository, fs: FileSystemPort, audit: Optional[AuditPort] = None):
        self.settings_repo = settings_repo
        self.fs = fs
        self.audit = audit

    def delete_projects(self, project_names: list[str], scope: ProjectType, actor: str = '') -> dict:
        settings = self.settings_repo.get_all_settings()
        path_key = 'online_path' if scope == ProjectType.ONLINE else 'gaveta_path'
        metadata_base = settings.get(path_key, '').strip()
        av_medias_base = settings.get('av_medias_a_path', '').strip()

        done = []
        failed = []

        for name in project_names:
            try:
                if metadata_base:
                    meta_path = os.path.join(metadata_base, name)
                    if self.fs.directory_exists(meta_path):
                        self.fs.delete_directory(meta_path)

                if av_medias_base:
                    media_path = os.path.join(av_medias_base, name)
                    if self.fs.directory_exists(media_path):
                        self.fs.delete_directory(media_path)

                done.append(name)
                EventBus.publish(ProjetoDeletado(project_name=name, scope=scope.value))
                if self.audit:
                    self.audit.log(actor, f'projeto-deletado:{name}:{scope.value}')
            except Exception as e:
                logger.error('Erro ao deletar projeto %s: %s', name, e)
                failed.append({'name': name, 'error': str(e)})

        return {
            'success': len(failed) == 0,
            'message': f'{len(done)} projeto(s) removidos.' if not failed else f'Removidos {len(done)}, falha em {len(failed)}.',
            'done': done,
            'failed': failed,
        }

    def engavetar_projects(self, project_names: list[str], actor: str = '') -> dict:
        settings = self.settings_repo.get_all_settings()
        online_base = settings.get('online_path', '').strip()
        gaveta_base = settings.get('gaveta_path', '').strip()

        if not online_base or not self.fs.directory_exists(online_base):
            return {'success': False, 'message': 'Caminho ONLINE inválido.'}
        if not gaveta_base or not self.fs.directory_exists(gaveta_base):
            return {'success': False, 'message': 'Caminho GAVETA inválido.'}

        done = []
        failed = []

        for name in project_names:
            src = os.path.join(online_base, name)
            dst = os.path.join(gaveta_base, name)
            try:
                if self.fs.directory_exists(src):
                    self.fs.move_directory(src, dst)
                    done.append(name)
                    EventBus.publish(ProjetoEngavetado(project_name=name))
                    if self.audit:
                        self.audit.log(actor, f'projeto-engavetado:{name}')
                else:
                    failed.append({'name': name, 'error': 'Pasta não encontrada na origem.'})
            except Exception as e:
                logger.error('Erro ao engavetar projeto %s: %s', name, e)
                failed.append({'name': name, 'error': str(e)})

        return {
            'success': len(failed) == 0,
            'message': f'{len(done)} projeto(s) engavetados.' if not failed else f'Engavetados {len(done)}, falha em {len(failed)}.',
            'done': done,
            'failed': failed,
        }

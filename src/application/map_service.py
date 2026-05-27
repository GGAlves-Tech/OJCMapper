import os
from domain import SettingsRepository
from domain.interfaces import DriveMapper
from domain.shared.events import EventBus, UnidadeMapeada, UnidadeDesconectada


class MapUseCase:
    def __init__(self, settings_repo: SettingsRepository, mapper: DriveMapper):
        self.settings_repo = settings_repo
        self.mapper = mapper

    def map_project(self, project_name: str) -> tuple[bool, str, str]:
        if not project_name:
            return False, 'Nome do projeto não informado.', ''

        settings = self.settings_repo.get_all_settings()
        av_medias_base = settings.get('av_medias_a_path', '')

        if not av_medias_base:
            return False, 'Caminho de Mídias (av_medias_a_path) não configurado.', ''

        network_path = os.path.join(av_medias_base, project_name).replace('/', '\\')
        letter = self.mapper.get_available_letter()

        if not letter:
            return False, 'Nenhuma letra de unidade disponível.', ''

        success, message = self.mapper.map_drive(letter, network_path)
        if success:
            EventBus.publish(UnidadeMapeada(project_name=project_name, drive_letter=letter))
        return success, message, letter if success else ''

    def unmap_project(self, drive_letter: str) -> tuple[bool, str]:
        success, message = self.mapper.unmap_drive(drive_letter)
        if success:
            EventBus.publish(UnidadeDesconectada(drive_letter=drive_letter))
        return success, message

    def get_active_drives(self) -> list[dict]:
        return self.mapper.get_mapped_drives()

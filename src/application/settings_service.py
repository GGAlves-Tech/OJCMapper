from domain import SettingsRepository


class SettingsUseCase:
    def __init__(self, settings_repo: SettingsRepository):
        self.settings_repo = settings_repo

    def get_settings(self) -> dict:
        return self.settings_repo.get_all_settings()

    def update_all(self, data: dict) -> None:
        for key, value in data.items():
            self.settings_repo.update_setting(key, value)

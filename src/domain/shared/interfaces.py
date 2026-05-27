from abc import ABC, abstractmethod


class SettingsRepository(ABC):
    @abstractmethod
    def get_all_settings(self) -> dict:
        pass

    @abstractmethod
    def update_setting(self, key: str, value: str) -> None:
        pass

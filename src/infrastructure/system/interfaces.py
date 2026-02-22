from abc import ABC, abstractmethod

class DriveMapper(ABC):
    @abstractmethod
    def get_available_letter(self) -> str | None:
        pass

    @abstractmethod
    def map_drive(self, drive_letter: str, network_path: str) -> tuple:
        pass

    @abstractmethod
    def unmap_drive(self, drive_letter: str) -> tuple:
        pass

    @abstractmethod
    def get_mapped_drives(self) -> list:
        pass

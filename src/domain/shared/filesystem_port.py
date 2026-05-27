from abc import ABC, abstractmethod


class FileSystemPort(ABC):
    @abstractmethod
    def list_directories(self, path: str) -> list[str]:
        pass

    @abstractmethod
    def directory_exists(self, path: str) -> bool:
        pass

    @abstractmethod
    def delete_directory(self, path: str) -> None:
        pass

    @abstractmethod
    def move_directory(self, src: str, dst: str) -> None:
        pass

    @abstractmethod
    def write_text_file(self, path: str, content: str) -> None:
        pass

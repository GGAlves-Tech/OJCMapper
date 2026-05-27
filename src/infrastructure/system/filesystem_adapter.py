import os
import shutil
from domain.interfaces import FileSystemPort


class LocalFileSystemAdapter(FileSystemPort):

    def list_directories(self, path: str) -> list[str]:
        try:
            return [
                item for item in os.listdir(path)
                if os.path.isdir(os.path.join(path, item))
            ]
        except Exception:
            return []

    def directory_exists(self, path: str) -> bool:
        return os.path.isdir(path)

    def delete_directory(self, path: str) -> None:
        shutil.rmtree(path)

    def move_directory(self, src: str, dst: str) -> None:
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.move(src, dst)

    def write_text_file(self, path: str, content: str) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

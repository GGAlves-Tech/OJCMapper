from abc import ABC, abstractmethod
from typing import List, Any, Optional

class BaseRepository(ABC):
    """ Interface base para repositórios seguindo o padrão Hexagonal """
    @abstractmethod
    def get_all(self) -> List[Any]:
        pass

    @abstractmethod
    def get_by_id(self, id: Any) -> Optional[Any]:
        pass

    @abstractmethod
    def add(self, entity: Any) -> None:
        pass

    @abstractmethod
    def update(self, entity: Any) -> None:
        pass

    @abstractmethod
    def delete(self, id: Any) -> None:
        pass

from domain.interfaces import BaseRepository
from typing import List, Any

class BaseUseCase:
    """ Classe base para casos de uso da aplicação """
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    def execute_list_all(self) -> List[Any]:
        return self.repository.get_all()

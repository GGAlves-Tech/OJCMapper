from abc import ABC, abstractmethod


class AuditPort(ABC):
    @abstractmethod
    def log(self, actor: str, action: str) -> None:
        pass

from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Dict, List, Type


class DomainEvent:
    """Classe base para todos os eventos de domínio."""
    pass


@dataclass(frozen=True)
class UsuarioCriado(DomainEvent):
    username: str
    role: str
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class UsuarioRemovido(DomainEvent):
    username: str
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class ProjetoEngavetado(DomainEvent):
    project_name: str
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class ProjetoDeletado(DomainEvent):
    project_name: str
    scope: str
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class UnidadeMapeada(DomainEvent):
    project_name: str
    drive_letter: str
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class UnidadeDesconectada(DomainEvent):
    drive_letter: str
    occurred_at: datetime = field(default_factory=datetime.now)


class EventBus:
    _handlers: Dict[Type[DomainEvent], List[Callable]] = {}

    @classmethod
    def subscribe(cls, event_type: Type[DomainEvent], handler: Callable) -> None:
        if event_type not in cls._handlers:
            cls._handlers[event_type] = []
        cls._handlers[event_type].append(handler)

    @classmethod
    def publish(cls, event: DomainEvent) -> None:
        for handler in cls._handlers.get(type(event), []):
            handler(event)

    @classmethod
    def clear(cls) -> None:
        cls._handlers.clear()

from dataclasses import dataclass, field
from datetime import datetime
from ..shared.domain_event import DomainEvent


@dataclass(frozen=True)
class UsuarioRemovido(DomainEvent):
    username: str
    occurred_at: datetime = field(default_factory=datetime.now)

from dataclasses import dataclass, field
from datetime import datetime
from ..shared.domain_event import DomainEvent


@dataclass(frozen=True)
class ProjetoDeletado(DomainEvent):
    project_name: str
    scope: str
    occurred_at: datetime = field(default_factory=datetime.now)

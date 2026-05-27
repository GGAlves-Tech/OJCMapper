from dataclasses import dataclass, field
from datetime import datetime
from ..shared.domain_event import DomainEvent


@dataclass(frozen=True)
class UnidadeMapeada(DomainEvent):
    project_name: str
    drive_letter: str
    occurred_at: datetime = field(default_factory=datetime.now)

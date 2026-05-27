from typing import Callable, Dict, List, Type
from .domain_event import DomainEvent


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

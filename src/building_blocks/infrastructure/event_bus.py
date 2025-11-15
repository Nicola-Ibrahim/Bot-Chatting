from __future__ import annotations

from collections import defaultdict
from typing import Callable, DefaultDict, Generic, Iterable, Type, TypeVar

from src.building_blocks.domain.events import DomainEvent

TDomainEvent = TypeVar("TDomainEvent", bound=DomainEvent)
EventHandler = Callable[[TDomainEvent], None]


class EventBus:
    """In-memory domain event bus with pub/sub semantics."""

    def __init__(self) -> None:
        self._subscribers: DefaultDict[Type[DomainEvent], list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_type: Type[TDomainEvent], handler: EventHandler[TDomainEvent]) -> None:
        self._subscribers[event_type].append(handler)  # type: ignore[arg-type]

    def publish(self, event: DomainEvent) -> None:
        for handler in self._subscribers.get(type(event), []):
            handler(event)  # type: ignore[arg-type]

    def publish_many(self, events: Iterable[DomainEvent]) -> None:
        for event in events:
            self.publish(event)

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Deque, Iterable
from collections import deque

from src.building_blocks.domain.events import DomainEvent


@dataclass
class OutboxMessage:
    """Represents a persisted domain event awaiting delivery."""

    id: uuid.UUID
    event_name: str
    payload: str
    occurred_on: datetime
    processed_at: datetime | None = None

    @classmethod
    def from_event(cls, event: DomainEvent) -> "OutboxMessage":
        return cls(
            id=event.id,
            event_name=event.__class__.__name__,
            payload=json.dumps(event.to_dict()),
            occurred_on=event.occurred_on,
        )


class Outbox:
    """In-memory outbox store suitable for tests and small services."""

    def __init__(self) -> None:
        self._messages: Deque[OutboxMessage] = deque()

    def add(self, event: DomainEvent) -> OutboxMessage:
        message = OutboxMessage.from_event(event)
        self._messages.append(message)
        return message

    def pending(self) -> list[OutboxMessage]:
        return [msg for msg in self._messages if msg.processed_at is None]

    def mark_processed(self, message_id: uuid.UUID) -> None:
        for message in self._messages:
            if message.id == message_id:
                message.processed_at = datetime.utcnow()
                break

    def drain(self) -> Iterable[OutboxMessage]:
        while self._messages:
            yield self._messages.popleft()

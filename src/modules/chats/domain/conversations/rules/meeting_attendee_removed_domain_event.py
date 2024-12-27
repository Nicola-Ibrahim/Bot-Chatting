import uuid
from dataclasses import dataclass, field
from datetime import datetime

from src.building_blocks.domain.events import DomainEvent


@dataclass
class MeetingAttendeeRemovedDomainEvent(DomainEvent):
    attendee_id: uuid.UUID
    conversation_id: uuid.UUID
    occurred_on: datetime = field(default_factory=datetime.now)

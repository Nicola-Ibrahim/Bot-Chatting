import uuid
from dataclasses import dataclass

from src.building_blocks.domain.events import DomainEvent


@dataclass
class OwnerActivatedEvent(DomainEvent):
    owner_id: uuid.UUID

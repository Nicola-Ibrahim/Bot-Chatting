import uuid
from dataclasses import dataclass

from src.building_blocks.domain.events import DomainEvent


@dataclass
class CreatorDeactivatedEvent(DomainEvent):
    creator_id: uuid.UUID

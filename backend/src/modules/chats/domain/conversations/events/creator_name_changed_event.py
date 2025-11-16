import uuid
from dataclasses import dataclass

from src.building_blocks.domain.events import DomainEvent


@dataclass
class CreatorNameChangedEvent(DomainEvent):
    creator_id: uuid.UUID
    new_name: str

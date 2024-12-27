import uuid
from dataclasses import dataclass

from src.building_blocks.domain.events import DomainEvent


@dataclass
class OwnerNameChangedEvent(DomainEvent):
    owner_id: uuid.UUID
    new_name: str

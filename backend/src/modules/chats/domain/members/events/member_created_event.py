from dataclasses import dataclass

from src.building_blocks.domain.events import DomainEvent


@dataclass
class MemberCreatedEvent(DomainEvent):
    member_id: str
    member_name: str
    created_at: str

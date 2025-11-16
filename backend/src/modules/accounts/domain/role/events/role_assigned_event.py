"""Event emitted when a role is assigned to an account."""

from dataclasses import dataclass

from src.building_blocks.domain.events import DomainEvent


@dataclass(slots=True)
class RoleAssignedEvent(DomainEvent):
    role_id: str
    account_id: str

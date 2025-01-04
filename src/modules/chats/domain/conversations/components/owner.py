from dataclasses import dataclass

from src.building_blocks.domain.entity import Entity
from src.modules.chats.domain.conversations.events import (
    OwnerActivatedEvent,
    OwnerDeactivatedEvent,
    OwnerNameChangedEvent,
)

from ...members.components.member_id import MemberId


@dataclass
class Owner(Entity):
    _name: str
    _is_active: bool = True

    @classmethod
    def create(cls, member_id: MemberId, name: str) -> "Owner":
        """
        Creates a new instance of the Owner class.

        Args:
            member_id (MemberId): The ID of the user.
            name (str): The name of the owner.

        Returns:
            Owner: A new instance of the Owner class.
        """
        return cls(_id=member_id, _name=name)

    def change_name(self, new_name: str) -> None:
        """
        Changes the name of the owner.

        Args:
            new_name (str): The new name of the owner.
        """
        self.check_rule(OwnerNameCannotBeEmptyRule(new_name))
        self.name = new_name
        self.add_event(OwnerNameChangedEvent(self.id, new_name))

    def deactivate(self) -> None:
        """
        Deactivates the owner.
        """
        self.is_active = False
        self.add_event(OwnerDeactivatedEvent(self.id))

    def activate(self) -> None:
        """
        Activates the owner.
        """
        self.is_active = True
        self.add_event(OwnerActivatedEvent(self.id))

    def is_owner_active(self) -> bool:
        """
        Checks if the owner is active.

        Returns:
            bool: True if the owner is active, False otherwise.
        """
        return self.is_active

from dataclasses import dataclass

from src.building_blocks.domain.entity import Entity

from ...members.value_objects.member_id import MemberId
from ..events import (
    CreatorDeactivatedEvent,
    CreatorNameChangedEvent,
)
from ..rules import CreatorNameCannotBeEmptyRule


@dataclass
class Creator(Entity):
    _id: MemberId
    _name: str
    _is_active: bool = True

    @classmethod
    def create(cls, id: MemberId, name: str) -> "Creator":
        """
        Creates a new instance of the Creator class.

        Args:
            id (MemberId): The ID of the user.
            name (str): The name of the creator.

        Returns:
            Creator: A new instance of the Creator class.
        """
        return cls(_id=id, _name=name)

    def change_name(self, new_name: str) -> None:
        """
        Changes the name of the creator.

        Args:
            new_name (str): The new name of the creator.
        """
        self.check_rule(CreatorNameCannotBeEmptyRule(new_name))
        self.name = new_name
        self.add_event(CreatorNameChangedEvent(self.id, new_name))

    def deactivate(self) -> None:
        """
        Deactivates the creator.
        """
        self.is_active = False
        self.add_event(CreatorDeactivatedEvent(self.id))

    def activate(self) -> None:
        """
        Activates the creator.
        """
        self.is_active = True
        self.add_event((self.id))

    def is__active(self) -> bool:
        """
        Checks if the creator is active.

        Returns:
            bool: True if the creator is active, False otherwise.
        """
        return self.is_active

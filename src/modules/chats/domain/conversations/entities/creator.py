from dataclasses import dataclass, field
from uuid import UUID

from src.building_blocks.domain.entity import Entity
from src.building_blocks.domain.exception import BusinessRuleValidationException

from ...members.value_objects.member_id import MemberId
from ..rules import CreatorNameCannotBeEmptyRule


@dataclass
class Creator(Entity):
    _id: MemberId
    _name: str
    _is_active: bool = field(default=True, init=False)

    @classmethod
    def create(cls, member_id: MemberId, name: str) -> "Creator":
        """
        Creates a new instance of the Creator class.

        Args:
            member_id (MemberId): The ID of the user.
            name (str): The name of the creator.

        Returns:
            Creator: A new instance of the Creator class.
        """
        cls.check_rules(CreatorNameCannotBeEmptyRule(name))
        return cls(_id=member_id, _name=name)

    def change_name(self, new_name: str) -> None:
        """
        Changes the name of the creator.

        Args:
            new_name (str): The new name of the creator.
        """
        self.check_rules(CreatorNameCannotBeEmptyRule(new_name))
        self._name = new_name
        self.add_event(CreatorNameChangedEvent(self._id, new_name))

    def deactivate(self) -> None:
        """
        Deactivates the creator.
        """
        self._is_active = False
        self.add_event(CreatorDeactivatedEvent(self._id))

    def activate(self) -> None:
        """
        Activates the creator.
        """
        self._is_active = True
        self.add_event(CreatorActivatedEvent(self._id))

    @property
    def is_active(self) -> bool:
        """
        Checks if the creator is active.

        Returns:
            bool: True if the creator is active, False otherwise.
        """
        return self._is_active

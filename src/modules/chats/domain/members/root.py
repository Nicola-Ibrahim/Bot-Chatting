import uuid
from dataclasses import KW_ONLY, dataclass, field
from datetime import datetime, timezone
from typing import Self

from src.building_blocks.domain.entity import AggregateRoot

from .events import MemberCreatedEvent
from .value_objects.member_id import MemberId


@dataclass(kw_only=True, slots=True)
class Member(AggregateRoot):
    """
    Represents a chat member. Contains the member's ID, first name, last name, and roles.
    """

    _id: MemberId
    _first_name: str
    _last_name: str
    _is_admin: bool = False
    _is_creator: bool = False
    _created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def id(self) -> MemberId:
        return self._id

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def is_admin(self) -> bool:
        return self._is_admin

    @property
    def is_creator(self) -> bool:
        return self._is_creator

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @classmethod
    def create(
        cls, id: uuid.UUID, first_name: str, last_name: str, is_admin: bool = False, is_creator: bool = False
    ) -> Self:
        """
        Factory method to create a new member instance with validation.

        Args:
            id (uuid.UUID): The unique identifier for the member.
            first_name (str): The first name of the member.
            last_name (str): The last name of the member.
            is_admin (bool, optional): Whether the member is an admin. Defaults to False.
            is_creator (bool, optional): Whether the member is the creator. Defaults to False.

        Returns:
            Member: A new instance of the Member class.
        """
        cls.check_rules(
            # Add any specific business rules here if needed
        )
        member = cls(
            _id=MemberId.create(id),
            _first_name=first_name,
            _last_name=last_name,
            _is_admin=is_admin,
            _is_creator=is_creator,
        )
        member.add_event(
            MemberCreatedEvent(
                member_id=id, member_name=f"{first_name} {last_name}", created_at=str(member.created_at)
            )
        )
        return member

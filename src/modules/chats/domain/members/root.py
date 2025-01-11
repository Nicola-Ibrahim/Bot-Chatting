import uuid
from dataclasses import dataclass

from src.building_blocks.domain.entity import AggregateRoot

from .events import MemberCreatedEvent
from .value_objects.member_id import MemberId


@dataclass
class Member(AggregateRoot):
    """
    Represents a chat member. Contains the member's ID, chat ID, and user ID.
    """

    _id: MemberId
    _first_name: str
    _last_name: str
    _is_admin: bool = False
    _is_creator: bool = False

    @classmethod
    def create(cls, id: uuid.UUID, first_name: str, last_name: str, is_admin: bool, is_creator: bool) -> "Member":
        member = cls(
            _id=MemberId(value=id),
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

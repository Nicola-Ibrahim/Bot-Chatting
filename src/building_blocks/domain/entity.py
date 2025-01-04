import datetime
from dataclasses import asdict, dataclass, field
from typing import Any

from .events import DomainEvent
from .exception import BusinessRuleValidationException
from .rule import BaseBusinessRule


@dataclass
class Entity:
    """
    Abstract base class for all domain entities. Provides unique ID, equality checks,
    copy functionality, and serialization support.
    Supports flexible ID types.
    """

    _id: str
    _events: list[DomainEvent] = field(default_factory=list)
    _created_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    @property
    def id(self) -> str:
        """
        Retrieves the ID of the conversation.

        Returns:
            ConversationId: The ID of the conversation.
        """
        return self._id

    @property
    def created_at(self) -> datetime.datetime:
        """Get the creation timestamp of the entity."""
        return self._created_at

    def __eq__(self, other: Any) -> bool:
        """Check equality based on the entity ID."""
        if not isinstance(other, Entity):
            return False
        return self._id == other._id

    def add_event(self, event: DomainEvent) -> None:
        """Add a domain event to the entity."""
        self._events.append(event)

    def clear_events(self) -> None:
        """Clear all domain events."""
        self._events.clear()

    def get_events(self) -> list[DomainEvent]:
        """Get all domain events."""
        return self._events

    def check_rule(self, rule: BaseBusinessRule) -> None:
        """Validate a business rule."""
        if not rule.is_satisfied():
            raise BusinessRuleValidationException(rule)

    def to_dict(self) -> dict:
        """Serialize the entity to a dictionary."""
        return asdict(self)


@dataclass
class AggregateRoot(Entity):
    """
    A special type of Entity that serves as the root of an aggregate in DDD.
    This class does not introduce additional logic, but it can be extended in the future.
    """

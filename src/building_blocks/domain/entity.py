import datetime
from dataclasses import asdict, dataclass, field
from itertools import count
from typing import Any

from .domain_event import DomainEvent
from .exception import BusinessRuleValidationException
from .identifier import Identifier
from .rule import BaseBusinessRule


@dataclass
class Entity:
    """
    Abstract base class for all domain entities. Provides unique ID, equality checks,
    copy functionality, and serialization support.
    Supports flexible ID types.
    """

    _id: Identifier
    _instance_count: int = field(default_factory=lambda: next(count()))
    _events: list[DomainEvent] = field(default_factory=list)
    _created_at: datetime = field(default_factory=datetime.datetime.now(datetime.timezone.utc))

    @property
    def id(self) -> Identifier:
        """Get the ID of the entity."""
        return self._id

    @property
    def instance_count(self) -> int:
        """Get the instance-specific ID."""
        return self._instance_count

    @property
    def created_at(self):
        return self._created_at

    def __eq__(self, other: Any) -> bool:
        """
        Equality check based on ID. Ensures entities of the same type with the same ID are equal.
        """
        if isinstance(other, self.__class__):
            return self._id == other.id
        return False

    def __hash__(self) -> int:
        """
        Hashing based on the entity's ID.
        """
        return hash(self._id)

    def __repr__(self) -> str:
        """
        String representation including entity's ID and instance ID.
        """
        return f"<{self.__class__.__name__}(id={self._id}, instance_count={self._instance_count})>"

    def copy(self, **changes) -> "Entity":
        """
        Create a copy of the entity, allowing specific attributes to be modified.
        This can be useful for creating a new version of the entity with updates.
        """
        updated_data = asdict(self)
        updated_data.update(changes)
        return self.__class__(**updated_data)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the entity to a dictionary representation for easy serialization.
        This will recursively serialize any nested `Entity` objects as well.
        """
        return {key: (value.to_dict() if isinstance(value, Entity) else value) for key, value in asdict(self).items()}

    @classmethod
    def create(cls, **kwargs) -> "Entity":
        """
        Factory method for creating a new instance of an entity.
        Subclasses should override this to apply business logic or constraints.
        """
        return cls(**kwargs)

    def _record_event(self, event: DomainEvent):
        self._events.append(event)

    def collect_events(self) -> list[DomainEvent]:
        events = self._events[:]
        self._events = []
        return events

    def check_rule(self, rule: BaseBusinessRule):
        if not rule.is_valid():
            raise BusinessRuleValidationException(rule)


@dataclass
class AggregateRoot(Entity):
    """
    A special type of Entity that serves as the root of an aggregate in DDD.
    This class does not introduce additional logic, but it can be extended in the future.
    """

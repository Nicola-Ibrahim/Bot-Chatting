import abc
import dataclasses
from itertools import count
from typing import Any
from uuid import UUID


@dataclasses.dataclass
class Entity(metaclass=abc.ABCMeta):
    """
    Abstract base class for all domain entities. Provides unique ID,
    equality checks, copy functionality, and serialization support.
    """

    _instance_id_generator = count()

    _id: UUID
    _instance_id: int = next(_instance_id_generator)

    def __eq__(self, other: Any) -> bool:
        """
        Check equality based on type and unique ID.
        """
        if isinstance(other, self.__class__):
            return self._id == other.id
        return False

    def __hash__(self) -> int:
        """
        Hash based on the unique ID, allowing entities to be used in hash-based collections.
        """
        return hash(self._id)

    def __repr__(self) -> str:
        """
        Provide a readable string representation of the entity, including its ID.
        """
        return f"<{self.__class__.__name__}(id={self._id})>"

    def copy(self, **changes) -> "Entity":
        """
        Create a copy of the entity, allowing specific attributes to be modified.
        This can be useful for creating a new version of the entity with updates.
        """
        updated_data = dataclasses.asdict(self)
        updated_data.update(changes)
        return self.__class__(**updated_data)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the entity to a dictionary representation for easy serialization.
        """
        return {
            key: (value.to_dict() if isinstance(value, Entity) else value)
            for key, value in dataclasses.asdict(self).items()
        }

    @property
    def id(self):
        return self._id

    @property
    def instance_id(self):
        return self._instance_id

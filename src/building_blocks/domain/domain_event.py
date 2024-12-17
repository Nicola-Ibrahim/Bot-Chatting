import datetime
import uuid
from dataclasses import dataclass, field


@dataclass
class DomainEvent:
    """Base class for the domain event"""

    _id: uuid.UUID = field(default_factory=uuid.uuid4)
    _occurred_on: datetime = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def occurred_on(self) -> datetime:
        return self._occurred_on

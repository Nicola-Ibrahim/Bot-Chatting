from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from sqlalchemy.engine import Engine

@dataclass
class DatabaseConnector(ABC):
    """Abstract base class for database connectors."""
    connection_string: str = None
    config: dict[str, str] = None
    kwargs: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.connection_string and not self.config:
            raise ValueError("Either connection_string or config must be provided")

    @abstractmethod
    def create_engine(self) -> Engine:
        """Create a SQLAlchemy engine."""
        pass

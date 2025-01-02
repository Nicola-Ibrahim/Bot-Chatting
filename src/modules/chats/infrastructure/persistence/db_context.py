from dataclasses import dataclass, field
from typing import Optional

from sqlmodel import Session, SQLModel, create_engine

from .db_models import Conversation, Member
from .db_set import DBSet


@dataclass
class DBContext:
    """Manages repositories and session lifecycle for database operations."""

    connection_string: str  # e.g.: "sqlite:///./chat.db"
    engine: Optional[Session] = field(init=False, default=None)
    session: Optional[Session] = field(init=False, default=None)

    # Repositories for specific models
    conversations: DBSet[Conversation] = field(init=False)
    members: DBSet[Member] = field(init=False)

    def __post_init__(self) -> None:
        """Initialize the database engine, session, and repositories."""
        self._initialize_engine()
        self._initialize_session()
        self._initialize_repositories()
        self._create_schema()

    def _initialize_engine(self) -> None:
        """Set up the database engine."""
        self.engine = create_engine(self.connection_string, echo=True)

    def _initialize_session(self) -> None:
        """Set up the session for database operations."""
        self.session = Session(self.engine)

    def _initialize_repositories(self) -> None:
        """Create repositories for each model."""
        self.conversations = DBSet(self.session, Conversation)
        self.members = DBSet(self.session, Member)

    def _create_schema(self) -> None:
        """Generate database tables from the models."""
        SQLModel.metadata.create_all(self.engine)

    def close(self) -> None:
        """Close the database session."""
        if self.session:
            self.session.close()

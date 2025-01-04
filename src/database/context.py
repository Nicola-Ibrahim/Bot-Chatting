from dataclasses import dataclass, field
from typing import Dict, Generic, Optional, Type, TypeVar

from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel

from .connection import DatabaseConnectionManager

ModelType = TypeVar("ModelType", bound=SQLModel)


@dataclass
class DBContext(Generic[ModelType]):
    """Manages repositories and session lifecycle for database operations."""

    engine: Engine = field(init=False)
    connection_string: Optional[str] = None
    config: Optional[Dict[str, str]] = None
    kwargs: Dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Initialize the database engine."""
        self.engine = DatabaseConnectionManager.create_db_engine(
            connection_string=self.connection_string, config=self.config, **self.kwargs
        )
        self._create_schema()
        self._set_engine_for_models()

    def _create_schema(self) -> None:
        """Generate database tables from the models."""
        SQLModel.metadata.create_all(self.engine)

    def _set_engine_for_models(self) -> None:
        """Set the engine for all models in the context."""
        for model in SQLModel.metadata.tables.values():
            model_class = model.info.get("class")
            if model_class:
                model_class.set_manager(self.engine)

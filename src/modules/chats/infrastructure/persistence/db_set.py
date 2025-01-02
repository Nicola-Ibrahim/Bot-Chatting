from contextlib import contextmanager
from typing import Generic, List, Type, TypeVar

from sqlmodel import Session, SQLModel, select

ModelType = TypeVar("ModelType", bound=SQLModel)


class DBSet(Generic[ModelType]):
    """Generic repository implementing SQLModel and Unit of Work."""

    def __init__(self, session: Session, model: Type[ModelType]):
        self.session = session
        self.model = model

    def add(self, entity: ModelType) -> None:
        """Add an entity to the session and commit."""
        self.session.add(entity)
        self.session.commit()

    def remove(self, entity: ModelType) -> None:
        """Remove an entity from the session and commit."""
        self.session.delete(entity)
        self.session.commit()

    def get(self, entity_id: int) -> ModelType | None:
        """Retrieve an entity by its ID."""
        return self.session.get(self.model, entity_id)

    def all(self) -> List[ModelType]:
        """Retrieve all entities."""
        statement = select(self.model)
        return self.session.exec(statement).all()

    def filter(self, **kwargs) -> List[ModelType]:
        """Retrieve entities that match filter criteria."""
        statement = select(self.model).filter_by(**kwargs)
        return self.session.exec(statement).all()

    def first(self, **kwargs) -> ModelType | None:
        """Retrieve the first entity that matches filter criteria."""
        statement = select(self.model).filter_by(**kwargs)
        return self.session.exec(statement).first()

    @contextmanager
    def transaction(self):
        """Provide a transactional scope."""
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

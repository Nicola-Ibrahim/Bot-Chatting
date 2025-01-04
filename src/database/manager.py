from typing import Generic, Type, TypeVar

from sqlmodel import Session, SQLModel, select

ModelType = TypeVar("ModelType", bound=SQLModel)


class Manager(Generic[ModelType]):
    def __init__(self, engine):
        self.engine = engine

    def add(self, entity: ModelType) -> None:
        """Add an entity to the session and commit."""
        with Session(self.engine) as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)

    def add_all(self, entities: list[ModelType]) -> None:
        """Add multiple entities to the session and commit."""
        with Session(self.engine) as session:
            session.add_all(entities)
            session.commit()

    def remove(self, entity: ModelType) -> None:
        """Remove an entity from the session and commit."""
        with Session(self.engine) as session:
            session.delete(entity)
            session.commit()

    def remove_all(self, entities: list[ModelType]) -> None:
        """Remove multiple entities from the session and commit."""
        with Session(self.engine) as session:
            for entity in entities:
                session.delete(entity)
            session.commit()

    def get(self, entity_id: int) -> ModelType | None:
        """Retrieve an entity by its ID."""
        with Session(self.engine) as session:
            return session.get(self.model, entity_id)

    def all(self) -> list[ModelType]:
        """Retrieve all entities."""
        with Session(self.engine) as session:
            statement = select(self.model)
            return session.exec(statement).all()

    def filter(self, **kwargs) -> list[ModelType]:
        """Retrieve entities that match filter criteria."""
        with Session(self.engine) as session:
            statement = select(self.model).filter_by(**kwargs)
            return session.exec(statement).all()

    def first(self, **kwargs) -> ModelType | None:
        """Retrieve the first entity that matches filter criteria."""
        with Session(self.engine) as session:
            statement = select(self.model).filter_by(**kwargs)
            return session.exec(statement).first()

    def paginate(self, page: int, per_page: int) -> list[ModelType]:
        """Retrieve a paginated list of entities."""
        with Session(self.engine) as session:
            statement = select(self.model).offset((page - 1) * per_page).limit(per_page)
            return session.exec(statement).all()

    def update(self, entity: ModelType) -> None:
        """Update an entity in the session and commit."""
        with Session(self.engine) as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)

from datetime import datetime, timezone

from sqlmodel import Field, SQLModel

from .manager import Manager


class TableMeta(type(SQLModel)):
    """
    Metaclass to automatically configure classes inheriting from SQLModel.

    This metaclass ensures that any subclass of `Model` is automatically registered
    as a database table unless explicitly marked as abstract with `__abstract__ = True`.
    """

    def __new__(cls, name, bases, dct):
        """
        Overrides the class creation process to add custom table settings.

        Args:
            cls: The metaclass itself.
            name (str): The name of the new class being created.
            bases (tuple): The base classes of the new class.
            dct (dict): The dictionary containing class attributes.

        Returns:
            The newly created class.
        """
        # Check if the class is marked as abstract
        if dct.get("__abstract__", False):
            # Skip configuring the table for abstract classes
            return super().__new__(cls, name, bases, dct)

        # Optional: Set table arguments (e.g., to extend existing tables)
        dct["__table_args__"] = {"extend_existing": True}

        # Automatically mark the class as a table
        dct["__config__"] = {"table": True}

        # Create the new class
        return super().__new__(cls, name, bases, dct)


class Model(SQLModel, metaclass=TableMeta):
    """
    Base model class for SQLModel with shared functionality.

    This class serves as a base for all models in the application and provides:
    - Common fields like `id`, `created_at`, and `updated_at`.
    - Automatic table registration via the `TableMeta` metaclass.
    - Integration with a `Manager` for managing database operations.
    """

    __abstract__ = True

    id: int | None = Field(default=None, primary_key=True, index=True)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    manager: Manager = Field(default=None, init=False)

    def __post_init__(self):
        """
        Post-initialization hook to update the `updated_at` timestamp.
        Ensures the field reflects the most recent state.
        """
        self.updated_at = datetime.now(timezone.utc)

    @classmethod
    def set_manager(cls, engine):
        """
        Sets the manager for the model using the provided database engine.

        Args:
            engine: The database engine to be used by the manager.
        """
        cls.manager = Manager(cls, engine)

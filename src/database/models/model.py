from datetime import datetime, timezone
from typing import TypeVar

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

from .manager import Manager

T = TypeVar("T", bound="BaseModel")

# SQLAlchemy's Base for declarative class definitions
Base = declarative_base()


class ManagerDescriptor:
    def __init__(self, manager_class: type[Manager]):
        self.manager_class = manager_class
        self._instance = None

    def __get__(self, obj, objtype):
        if self._instance is None:
            self._instance = self.manager_class(objtype)
        return self._instance


class BaseModelMeta(type):
    def __new__(cls, name, bases, dct):
        # Check if a custom manager is provided
        custom_manager = dct.get("manager", None)

        # If no custom manager, assign the default Manager
        if custom_manager is None:
            dct["manager"] = ManagerDescriptor(Manager)
        else:
            # If a custom manager is provided, wrap it in ManagerDescriptor
            if not isinstance(custom_manager, ManagerDescriptor):
                dct["manager"] = ManagerDescriptor(custom_manager)

        # Create the class with the manager
        return super().__new__(cls, name, bases, dct)


class BaseModel(Base, metaclass=BaseModelMeta):
    __abstract__ = True  # Mark as abstract, no direct instantiation

    # SQLAlchemy column definitions
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.updated_at = datetime.now(timezone.utc)

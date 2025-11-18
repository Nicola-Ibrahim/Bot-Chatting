from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy's Base for declarative class definitions
Base = declarative_base()


class BaseSQLModel(Base):
    __abstract__ = True  # Mark as abstract, no direct instantiation

    # SQLAlchemy column definitions
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.updated_at = datetime.now(timezone.utc)

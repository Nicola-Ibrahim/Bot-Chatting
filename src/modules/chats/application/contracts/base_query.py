import uuid
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

TResult = TypeVar("TResult")


class BaseQuery(BaseModel, Generic[TResult]):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)

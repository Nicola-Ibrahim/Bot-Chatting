import uuid
from abc import ABC
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from .iquery import IQuery

TResult = TypeVar("TResult")


class QueryBase(ABC, BaseModel, IQuery, Generic[TResult]):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)

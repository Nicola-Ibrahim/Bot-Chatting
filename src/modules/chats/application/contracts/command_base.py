import uuid
from abc import ABC
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from .icommand import ICommand

TResult = TypeVar("TResult")


class CommandBase(BaseModel, ABC, ICommand[TResult], Generic[TResult]):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)

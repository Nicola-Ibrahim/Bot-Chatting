from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Generic, Protocol, TypeVar, runtime_checkable

TCommandResult = TypeVar("TCommandResult")


@dataclass(slots=True)
class Command:
    """Base type for application commands."""

    id: uuid.UUID = field(default_factory=uuid.uuid4)


TCommand = TypeVar("TCommand", bound=Command)


@runtime_checkable
class CommandHandler(Protocol, Generic[TCommand, TCommandResult]):
    """Protocol for synchronous command handlers."""

    def handle(self, command: TCommand) -> TCommandResult: ...

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ..contracts.command import BaseCommand

TResult = TypeVar("TResult")
TCommand = TypeVar("TCommand", bound=BaseCommand)


class BaseCommandHandler(Generic[TCommand, TResult | None], ABC):
    @abstractmethod
    def handle(self, command: TCommand) -> TResult | None:
        pass

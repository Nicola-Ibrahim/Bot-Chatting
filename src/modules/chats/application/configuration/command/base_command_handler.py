from abc import ABC, abstractmethod
from typing import Generic, TypeVar

# Generic type variable for the result
TResult = TypeVar("TResult")


class BaseCommandHandler(Generic[TResult], ABC):
    @abstractmethod
    def handle(self, command):
        pass

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TResult = TypeVar("TResult")


class ICommand(ABC, Generic[TResult]):
    @abstractmethod
    def execute(self) -> TResult:
        pass

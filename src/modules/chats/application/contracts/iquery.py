from abc import ABC, abstractmethod
from typing import TypeVar, Generic

TResult = TypeVar('TResult')

class IQuery(ABC, Generic[TResult]):
    @abstractmethod
    def execute(self) -> TResult:
        pass
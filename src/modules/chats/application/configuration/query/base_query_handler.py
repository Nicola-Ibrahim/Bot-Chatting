from abc import ABC, abstractmethod
from typing import Generic, TypeVar

# Generic type for query results
TResult = TypeVar("TResult")


class BaseQueryHandler(Generic[TResult], ABC):
    @abstractmethod
    def handle(self, query):
        pass

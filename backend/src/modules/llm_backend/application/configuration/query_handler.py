from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ..contracts.query import BaseQuery

TResult = TypeVar("TResult")
TQuery = TypeVar("TQuery", bound=BaseQuery)


class BaseQueryHandler(Generic[TQuery, TResult], ABC):
    @abstractmethod
    def handle(self, query: TQuery) -> TResult:
        pass

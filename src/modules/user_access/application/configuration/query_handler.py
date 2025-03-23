from abc import ABC, abstractmethod
from typing import Any

from ..contracts.query import BaseQuery


class BaseQueryHandler(ABC):
    @abstractmethod
    def handle(self, query: BaseQuery) -> Any:
        pass

from abc import ABC, abstractmethod
from typing import TypeVar

from src.building_blocks.domain.result import Result

from .command import BaseCommand
from .query import BaseQuery

TResult = TypeVar("TResult")


class IMediator(ABC):
    @abstractmethod
    def execute_command(self, command: BaseCommand) -> Result:
        pass

    @abstractmethod
    def execute_query(self, query: BaseQuery) -> Result:
        pass

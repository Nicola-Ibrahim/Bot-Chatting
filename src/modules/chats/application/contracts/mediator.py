from abc import ABC, abstractmethod

from src.building_blocks.domain.result import Result, TError, TResult

from .command import BaseCommand
from .query import BaseQuery


class IMediator(ABC):
    @abstractmethod
    def execute_command(self, command: BaseCommand[TResult, TError]) -> Result[TResult, TError]:
        pass

    @abstractmethod
    def execute_query(self, query: BaseQuery[TResult, TError]) -> Result[TResult, TError]:
        pass

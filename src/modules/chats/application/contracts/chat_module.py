from abc import ABC, abstractmethod

from src.building_blocks.domain.result import TResult

from .command import BaseCommand
from .query import BaseQuery


class IChatModule(ABC):
    @abstractmethod
    async def execute_command_async(self, command: BaseCommand) -> TResult:
        raise NotImplementedError

    @abstractmethod
    async def execute_query_async(self, query: BaseQuery) -> TResult:
        raise NotImplementedError

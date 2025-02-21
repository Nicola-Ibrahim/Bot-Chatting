from abc import ABC, abstractmethod
from typing import TypeVar

from shared.infra.utils.result import Result

from .command import BaseCommand
from .query import BaseQuery

TResult = TypeVar("TResult")


class AbstractAIMediator(ABC):
    @abstractmethod
    async def execute_command(self, command: BaseCommand[TResult]) -> TResult:
        pass

    @abstractmethod
    async def execute_query(self, query: BaseQuery[TResult]) -> TResult:
        pass

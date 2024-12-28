from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from shared.infra.utils.result import Result

TResult = TypeVar("TResult")


class ICommand(Generic[TResult], ABC):
    pass


class IQuery(Generic[TResult], ABC):
    pass


class IChatsMediator(ABC):
    @abstractmethod
    async def execute_command(self, command: ICommand[TResult]) -> TResult:
        pass

    @abstractmethod
    async def execute_query(self, query: IQuery[TResult]) -> TResult:
        pass

from __future__ import annotations

from typing import Dict, Generic, Type, TypeVar

from .command import Command, CommandHandler
from .query import Query, QueryHandler


C = TypeVar("C", bound=Command)
Q = TypeVar("Q", bound=Query)
CommandResult = TypeVar("CommandResult")
QueryResult = TypeVar("QueryResult")


class CommandBus(Generic[C, CommandResult]):
    """Very small synchronous command bus."""

    def __init__(self) -> None:
        self._handlers: Dict[Type[C], CommandHandler[C, CommandResult]] = {}

    def register(self, command_type: Type[C], handler: CommandHandler[C, CommandResult]) -> None:
        self._handlers[command_type] = handler

    def dispatch(self, command: C) -> CommandResult:
        handler = self._handlers.get(type(command))
        if handler is None:
            raise LookupError(f"No handler registered for command {type(command).__name__}")
        return handler.handle(command)


class QueryBus(Generic[Q, QueryResult]):
    """Simple synchronous query bus."""

    def __init__(self) -> None:
        self._handlers: Dict[Type[Q], QueryHandler[Q, QueryResult]] = {}

    def register(self, query_type: Type[Q], handler: QueryHandler[Q, QueryResult]) -> None:
        self._handlers[query_type] = handler

    def ask(self, query: Q) -> QueryResult:
        handler = self._handlers.get(type(query))
        if handler is None:
            raise LookupError(f"No handler registered for query {type(query).__name__}")
        return handler.handle(query)

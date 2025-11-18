import asyncio
from typing import Any, Callable, Mapping, MutableMapping, Type

from src.modules.chats.application.contracts.command import BaseCommand
from src.modules.chats.application.contracts.mediator import IMediator
from src.modules.chats.application.contracts.query import BaseQuery

Handler = Callable[[Any], Any]


class Mediator(IMediator):
    """Lightweight mediator that routes commands/queries to registered handlers."""

    def __init__(self, handlers: Mapping[Type[Any], Handler] | None = None) -> None:
        self._handlers: MutableMapping[Type[Any], Handler] = dict(handlers or {})

    def register(self, message_type: Type[Any], handler: Handler) -> None:
        """Register or replace a handler for a given message type."""
        self._handlers[message_type] = handler

    def _dispatch(self, message: Any) -> Any:
        handler = self._handlers.get(type(message))
        if not handler:
            raise ValueError(f"No handler registered for {type(message)!r}")
        if hasattr(handler, "handle"):
            return handler.handle(message)  # type: ignore[no-any-return]
        return handler(message)

    async def send(self, message: Any) -> Any:
        """Async-friendly entry point used by the ChatsModule."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._dispatch, message)

    # IMediator compatibility -------------------------------------------------
    def execute_command(self, command: BaseCommand):
        return self._dispatch(command)

    def execute_query(self, query: BaseQuery):
        return self._dispatch(query)

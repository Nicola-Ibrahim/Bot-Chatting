from dependency_injector.wiring import Provide, inject

from src.building_blocks.domain.result import TResult

from ..application.contracts.chat_module import IChatsModule
from ..application.contracts.command import BaseCommand
from ..application.contracts.mediator import IMediator
from ..application.contracts.query import BaseQuery
from .configuration.di.containers import ChatDIContainer


class ChatsModule(IChatsModule):
    """Main entry point for the chats module"""

    @inject
    async def execute_command_async(
        self, command: BaseCommand, mediator: IMediator = Provide[ChatDIContainer.mediator]
    ) -> TResult:
        return await mediator.send(command)

    @inject
    async def execute_query_async(
        self, query: BaseQuery, mediator: IMediator = Provide[ChatDIContainer.mediator]
    ) -> TResult:
        return await mediator.send(query)

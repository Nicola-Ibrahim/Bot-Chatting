from dependency_injector.wiring import Provide, inject

from src.building_blocks.domain.result import TResult

from ..application.contracts.account_module import IAccountsModule
from ..application.contracts.command import BaseCommand
from ..application.contracts.mediator import IMediator
from ..application.contracts.query import BaseQuery
from .configuration.containers import AccountsDIContainer


class AccountsModule(IAccountsModule):
    """Main entry point for the accounts module"""

    @inject
    async def execute_command_async(
        self, command: BaseCommand, mediator: IMediator = Provide[AccountsDIContainer.mediator]
    ) -> TResult:
        return await mediator.send(command)

    @inject
    async def execute_query_async(
        self, query: BaseQuery, mediator: IMediator = Provide[AccountsDIContainer.mediator]
    ) -> TResult:
        return await mediator.send(query)

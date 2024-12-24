from src.building_blocks.domain.exception import BusinessRuleValidationException, RepositoryException
from src.building_blocks.domain.result import Result, resultify

from ....domain.interfaces.conversation_repository import AbstractConversationRepository
from ...configuration.command.base_command_handler import BaseCommandHandler
from .delete_conversation_command import DeleteConversationCommand


class DeleteConversationCommandHandler(BaseCommandHandler[DeleteConversationCommand]):
    def __init__(self, repository: AbstractConversationRepository):
        self._repository = repository

    @resultify
    def handle(self, command: DeleteConversationCommand) -> Result[None, str]:
        try:
            self._repository.delete(command.conversation_id)
            return None
        except (BusinessRuleValidationException, RepositoryException) as e:
            return e
            return e
            return e

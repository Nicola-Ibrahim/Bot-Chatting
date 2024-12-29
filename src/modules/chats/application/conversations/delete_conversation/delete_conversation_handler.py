from src.building_blocks.domain.exception import BusinessRuleValidationException, RepositoryException
from src.building_blocks.domain.result import Result, TError, resultify

from ....domain.conversations.interfaces.repository import AbstractConversationRepository
from ...configuration.command_handler import AbstractCommandHandler
from .delete_conversation_command import DeleteConversationCommand


class DeleteConversationCommandHandler(AbstractCommandHandler[DeleteConversationCommand, Result[None, TError]]):
    def __init__(self, repository: AbstractConversationRepository):
        self._repository = repository

    @resultify
    def handle(self, command: DeleteConversationCommand) -> Result[None, TError]:
        # The Result type encapsulates either a successful result (None) or an error of type TError
        try:
            self._repository.delete(command.conversation_id)
            return None
        except (BusinessRuleValidationException, RepositoryException) as e:
            return e

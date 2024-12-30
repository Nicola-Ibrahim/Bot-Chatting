from src.building_blocks.domain.exception import BusinessRuleValidationException, RepositoryException
from src.building_blocks.domain.result import Result, TError

from ....domain.conversations.interfaces.repository import AbstractConversationRepository
from ...configuration.command_handler import AbstractCommandHandler
from .delete_conversation_command import DeleteConversationCommand


class DeleteConversationCommandHandler(AbstractCommandHandler[DeleteConversationCommand, None]):
    def __init__(self, repository: AbstractConversationRepository):
        self._repository = repository

    def handle(self, command: DeleteConversationCommand) -> None:
        try:
            self._repository.delete(command.conversation_id)
            return None
        except (BusinessRuleValidationException, RepositoryException) as e:
            raise e

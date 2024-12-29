from src.building_blocks.domain.exception import BusinessRuleValidationException, RepositoryException
from src.building_blocks.domain.result import Result, TError, TResult, resultify

from ....domain.conversations.interfaces.repository import AbstractConversationRepository
from ....domain.conversations.root import Conversation
from ...configuration.command_handler import AbstractCommandHandler
from .create_conversation_command import CreateConversationCommand


class CreateNewConversationCommandHandler(AbstractCommandHandler[CreateConversationCommand, Result[TResult, TError]]):
    def __init__(self, repository: AbstractConversationRepository):
        self._repository = repository

    @resultify
    def handle(self, command: CreateConversationCommand) -> Result[TResult, TError]:
        # The Result type encapsulates either a successful result (TResult) or an error (TError).
        try:
            conversation = Conversation.create(
                user_id=command.user_id, user_name=command.user_name, title=command.conversation_title
            )
            self._repository.save(conversation)
            return conversation.id

        except (BusinessRuleValidationException, RepositoryException) as e:
            return e

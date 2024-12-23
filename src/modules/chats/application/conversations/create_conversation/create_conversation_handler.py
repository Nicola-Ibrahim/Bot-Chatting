from src.building_blocks.domain.exception import BusinessRuleValidationException, RepositoryException
from src.building_blocks.domain.result import Result, resultify
from src.modules.chats.domain.root import Conversation

from ....domain.interfaces.conversation_repository import AbstractConversationRepository
from ...application.services.conversation_dto import ConversationDTO
from ...configuration.command.base_command_handler import BaseCommandHandler
from .create_conversation_command import CreateConversationCommand


class CreateNewConversationCommandHandler(BaseCommandHandler[CreateConversationCommand]):
    def __init__(self, repository: AbstractConversationRepository):
        self._repository = repository

    @resultify
    def handle(self, command: CreateConversationCommand) -> Result[ConversationDTO, str]:
        try:
            conversation = Conversation.start(user_id=command.user_id)
            self._repository.save(conversation)
            return ConversationDTO.from_domain(conversation)
        except (BusinessRuleValidationException, RepositoryException) as e:
            return e
            return e
            return e

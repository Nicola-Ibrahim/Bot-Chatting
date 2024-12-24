from src.building_blocks.application.base_command_handler import BaseCommandHandler
from src.building_blocks.domain.exception import BusinessRuleValidationException, RepositoryException
from src.building_blocks.domain.result import Result, resultify
from src.modules.chats.domain.conversations.root import Conversation
from src.modules.chats.domain.messages.root import Message
from src.modules.chats.domain.value_objects import Content

from ....domain.interfaces.conversation_repository import AbstractConversationRepository
from ....infra.services.response_generator import ResponseGenerator
from ...application.services.conversation_dto import ConversationDTO


class AddMessageToConversationCommandHandler(BaseCommandHandler):
    def __init__(self, repository: AbstractConversationRepository, response_generator: ResponseGenerator):
        self._repository = repository
        self._response_generator = response_generator

    @resultify
    def handle(self, command: AddMessageToConversationCommand) -> Result[ConversationDTO, str]:
        try:
            response = self._response_generator.generate_answer(command.text)

            content = Content.create(text=command.text, response=response)
            conversation.add_message(content=content)
            Message.create(content=content)
            self._repository.save(conversation)

            return ConversationDTO.from_domain(conversation)

        except (BusinessRuleValidationException, RepositoryException) as e:
            return e
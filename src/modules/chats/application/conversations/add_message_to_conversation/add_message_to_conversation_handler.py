from src.building_blocks.domain.exception import BusinessRuleValidationException, RepositoryException
from src.building_blocks.domain.result import Result, resultify

from ....application.configuration.command.base_command_handler import BaseCommandHandler
from ....domain.conversations.root import
from ....domain.interfaces.conversation_repository import AbstractConversationRepository
from ....domain.messages.models.content import Content
from ....domain.messages.root import Message
from ....domain.value_objects import Content
from ....infra.services.response_generator import ResponseGenerator
from .add_message_to_conversation_command import AddMessageToConversationCommand

class AddMessageToConversationCommandHandler(BaseCommandHandler[AddMessageToConversationCommand]):
    def __init__(self, repository: AbstractConversationRepository, response_generator: ResponseGenerator):
        self._repository = repository
        self._response_generator = response_generator

    @resultify
    def handle(self, command: AddMessageToConversationCommand) -> Result[Message, Exception]:
        try:
            conversation = self._repository.get_by_id(command.conversation_id)
            response = self._response_generator.generate_answer(command.text)

            content = Content.create(text=command.text, response=response)
            conversation.add_message(content=content)
            message = Message.create(content=content)
            self._repository.save(conversation)

        except (BusinessRuleValidationException, RepositoryException) as e:
            return e

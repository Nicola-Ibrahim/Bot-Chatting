from src.building_blocks.domain.exception import BusinessRuleValidationException, RepositoryException
from src.modules.chats.domain.messages.root import Message

from ....domain.conversations.interfaces.repository import Conversations
from ....domain.messages.interfaces.repository import AbstractMessageRepository
from ....domain.messages.root import Message
from ....domain.messages.value_objects.content import Content
from ....infrastructure.services.response_generator import ResponseGenerator
from ...configuration.command_handler import AbstractCommandHandler
from .add_message_to_conversation_command import AddMessageToConversationCommand


class AddMessageToConversationCommandHandler(AbstractCommandHandler[AddMessageToConversationCommand, Message]):
    def __init__(
        self,
        conversation_repository: Conversations,
        messages_repository: AbstractMessageRepository,
        response_generator: ResponseGenerator,
    ):
        self._conversation_repository = conversation_repository
        self._messages_repository = messages_repository
        self._response_generator = response_generator

    def handle(self, command: AddMessageToConversationCommand) -> Message:
        conversation = self._conversation_repository.find(conversation_id=command.conversation_id)
        if not conversation:
            raise BusinessRuleValidationException("Conversation not found")

        response = self._response_generator.generate_answer(command.text)

        content = Content.create(text=command.text, response=response)
        message = Message.create(conversation_id=command.conversation_id, sender_id=command.user_id, content=content)

        conversation.add_message(content=content)

        self._conversation_repository.save(conversation=conversation)
        self._messages_repository.save(message=message)

        return message

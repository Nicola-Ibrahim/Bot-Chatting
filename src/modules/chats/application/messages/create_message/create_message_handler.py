from src.building_blocks.domain.exception import BusinessRuleValidationException, RepositoryException

from ....domain.conversations.value_objects.conversation_id import ConversationId
from ....domain.members.value_objects.member_id import MemberId
from ....domain.messages import AbstractMessageRepository
from ....domain.messages.root import Message
from ....domain.messages.value_objects.content import Content
from ....domain.messages.value_objects.message_id import MessageId
from ....infrastructure import ResponseGenerator
from ...configuration.command_handler import AbstractCommandHandler
from .create_message_command import CreateMessageCommand


class CreateMessageCommandHandler(AbstractCommandHandler[CreateMessageCommand, Message]):
    def __init__(
        self,
        messages_repository: AbstractMessageRepository,
        response_generator: ResponseGenerator,
    ):
        self._messages_repository = messages_repository
        self._response_generator = response_generator

    def handle(self, command: CreateMessageCommand) -> Message:
        # Generate a response
        response = self._response_generator.generate_answer(command.text)

        # Create value objects in the application layer
        conversation_id = ConversationId.create(command.conversation_id)
        sender_id = MemberId.create(command.user_id)
        content = Content.create(text=command.text, response=response)

        # Pass value objects to the domain layer
        message = Message.create(
            message_id=MessageId.create(),
            conversation_id=conversation_id,
            sender_id=sender_id,
            content=content,
        )

        # Save the message
        self._messages_repository.save(message=message)

        return message

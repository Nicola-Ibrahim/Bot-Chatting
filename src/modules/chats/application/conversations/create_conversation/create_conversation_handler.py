from ....domain.conversations.interfaces.repository import Conversations
from ....domain.conversations.root import Conversation
from ...configuration.command_handler import AbstractCommandHandler
from .create_conversation_command import CreateConversationCommand


class CreateNewConversationCommandHandler(AbstractCommandHandler[CreateConversationCommand, str]):
    def __init__(self, repository: Conversations):
        self._repository = repository

    def handle(self, command: CreateConversationCommand) -> str:
        conversation = Conversation.create(
            user_id=command.user_id, user_name=command.user_name, title=command.conversation_title
        )
        self._repository.save(conversation)
        return conversation.id

from ....domain.conversations.interfaces.repository import Conversations
from ...configuration.command_handler import AbstractCommandHandler
from .delete_conversation_command import DeleteConversationCommand


class DeleteConversationCommandHandler(AbstractCommandHandler[DeleteConversationCommand, None]):
    def __init__(self, conversation_repository: Conversations):
        self._conversation_repository = conversation_repository

    def handle(self, command: DeleteConversationCommand) -> None:
        self._conversation_repository.delete(command.conversation_id)
        return None

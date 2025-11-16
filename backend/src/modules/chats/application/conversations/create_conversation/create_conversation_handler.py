from ....domain.conversations.interfaces.repository import Conversations
from ....domain.conversations.root import Conversation
from ...configuration.command_handler import BaseCommandHandler
from .create_conversation_command import CreateConversationCommand


class CreateNewConversationCommandHandler(BaseCommandHandler):
    def __init__(self, repository: Conversations):
        self._repository = repository

    def handle(self, command: CreateConversationCommand) -> str:
        """
        Handle the creation of a new conversation by delegating to the domain model
        and persisting the resulting aggregate.

        Args:
            command: The command containing the necessary data to create a conversation.

        Returns:
            The identifier of the newly created conversation as a string.
        """
        conversation = Conversation.create(
            creator_id=command.user_id,
            creator_name=command.user_name,
            title=command.conversation_title,
        )
        self._repository.save(conversation)
        # Return string form of UUID for external consumption
        return str(conversation.id)

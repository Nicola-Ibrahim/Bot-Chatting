from uuid import UUID

from chats.domain.conversations.conversation import ConversationRepository
from chats.domain.messages.message import Message, MessageRepository

from src.building_blocks.domain.result import resultify


class GetSubOfMessagesQuery:
    def __init__(self, conversation_id: UUID, n: int):
        self.conversation_id = conversation_id
        self.n = n


class GetSubOfMessagesQueryHandler:
    def __init__(self, conversation_repository: ConversationRepository, message_repository: MessageRepository):
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository

    @resultify
    def handle(self, query: GetSubOfMessagesQuery) -> Result[list[Message], str]:
        """
        Handles the query to retrieve the last n messages for a given conversation.
        """
        conversation = self.conversation_repository.get_by_id(query.conversation_id)
        if not conversation:
            return Result.fail(f"Conversation with ID {query.conversation_id} not found")

        message_ids = conversation.get_last_n_messages(query.n)
        messages = [self.message_repository.get_by_id(message_id) for message_id in message_ids]
        if None in messages:
            return Result.fail("One or more messages could not be found")

        return Result.ok(messages)

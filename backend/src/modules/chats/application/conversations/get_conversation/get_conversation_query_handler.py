from ....domain.conversations.interfaces.repository import Conversations
from ...configuration.query_handler import BaseQueryHandler
from .get_conversation_dto import GetConversationDTO
from .get_conversation_query import GetConversationQuery


class GetConversationQueryHandler(BaseQueryHandler):
    def __init__(self, repository: Conversations):
        self._repository = repository

    def handle(self, query: GetConversationQuery) -> GetConversationDTO:
        """
        Handle the retrieval of a single conversation by delegating to the
        repository and mapping the result to a data transfer object (DTO).

        Args:
            query: A ``GetConversationQuery`` containing the conversation ID.

        Returns:
            A ``GetConversationDTO`` representing the conversation, or
            raises an exception if retrieval fails.
        """
        # Use the domain repository's ``find`` method to look up the
        # conversation aggregate by its identifier. The repository returns
        # ``None`` if no conversation exists with the given ID, so callers
        # may want to handle that scenario accordingly.
        conversation = self._repository.find(str(query.conversation_id))
        if conversation is None:
            raise ValueError(f"Conversation with ID {query.conversation_id} not found")
        return GetConversationDTO.from_domain(conversation)

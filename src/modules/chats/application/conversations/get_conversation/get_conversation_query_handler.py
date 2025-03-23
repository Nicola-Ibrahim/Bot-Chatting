from ....domain.conversations.interfaces.repository import Conversations
from ...configuration.query_handler import BaseQueryHandler
from .get_conversation_dto import GetConversationDTO
from .get_conversation_query import GetConversationQuery


class GetConversationQueryHandler(BaseQueryHandler):
    def __init__(self, repository: Conversations):
        self._repository = repository

    def handle(self, query: GetConversationQuery) -> GetConversationDTO:
        try:
            conversation = self._repository.get_by_id(query.conversation_id)
            return GetConversationDTO.from_domain(conversation)
        except Exception as e:
            raise e

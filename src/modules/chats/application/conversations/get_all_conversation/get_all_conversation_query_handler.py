from ....domain.conversations.interfaces.repository import Conversations
from ...configuration.query_handler import BaseQueryHandler
from .get_all_conversation_query import GetAllConversationsQuery


class GetAllConversationsQueryHandler(BaseQueryHandler):
    def __init__(self, conversation_repository: Conversations):
        self._conversation_repository = conversation_repository

    def handle(self, query: GetAllConversationsQuery) -> list[GetAllConversationsQuery]:
        try:
            conversations = self._conversation_repository.get_all()
            return [GetAllConversationsQuery.from_domain(conversation) for conversation in conversations]
        except Exception as e:
            raise e

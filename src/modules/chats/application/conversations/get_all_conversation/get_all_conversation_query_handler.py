from src.building_blocks.domain.result import resultify
from src.modules.chats.application.interfaces.conversation_repository import AbstractConversationRepository

from ...configuration.query.base_query_handler import BaseQueryHandler
from .get_all_conversation_query import GetAllConversationsQuery


class GetAllConversationsQueryHandler(BaseQueryHandler[GetAllConversationsQuery, list[GetAllConversationsQuery]]):
    def __init__(self, repository: AbstractConversationRepository):
        self._repository = repository

    @resultify
    def handle(self, query: GetAllConversationsQuery) -> list[GetAllConversationsQuery]:
        try:
            conversations = self._repository.get_all()
            return [GetAllConversationsQuery.from_domain(conversation) for conversation in conversations]
        except Exception as e:
            raise e

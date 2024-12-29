from src.building_blocks.domain.result import Result, TError, resultify

from ....domain.conversations.interfaces.repository import AbstractConversationRepository
from ...configuration.query_handler import AbstractQueryHandler
from .get_all_conversation_query import GetAllConversationsQuery


class GetAllConversationsQueryHandler(
    AbstractQueryHandler[GetAllConversationsQuery, Result[list[GetAllConversationsQuery], TError]]
):
    def __init__(self, repository: AbstractConversationRepository):
        self._repository = repository

    @resultify
    def handle(self, query: GetAllConversationsQuery) -> Result[list[GetAllConversationsQuery], TError]:
        try:
            conversations = self._repository.get_all()
            return [GetAllConversationsQuery.from_domain(conversation) for conversation in conversations]
        except Exception as e:
            raise e

from src.building_blocks.domain.result import resultify
from src.modules.chats.application.interfaces.conversation_repository import AbstractConversationRepository

from ...configuration.query.base_query_handler import BaseQueryHandler
from .get_conversation_dto import GetConversationDTO
from .get_conversation_query import GetConversationQuery


class GetConversationQueryHandler(BaseQueryHandler[GetConversationQuery, GetConversationDTO]):
    def __init__(self, repository: AbstractConversationRepository):
        self._repository = repository

    @resultify
    def handle(self, query: GetConversationQuery) -> GetConversationDTO:
        try:
            conversation = self._repository.get_by_id(query.conversation_id)
            return GetConversationDTO.from_domain(conversation)
        except Exception as e:
            raise e
            raise e

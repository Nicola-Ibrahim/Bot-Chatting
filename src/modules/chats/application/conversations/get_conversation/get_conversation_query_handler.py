from src.building_blocks.domain.result import Result, TError, resultify

from ....domain.conversations.interfaces.repository import AbstractConversationRepository
from ...configuration.query_handler import AbstractQueryHandler
from .get_conversation_dto import GetConversationDTO
from .get_conversation_query import GetConversationQuery


class GetConversationQueryHandler(AbstractQueryHandler[GetConversationQuery, Result[GetConversationDTO, TError]]):
    def __init__(self, repository: AbstractConversationRepository):
        self._repository = repository

    @resultify
    def handle(self, query: GetConversationQuery) -> Result[GetConversationDTO, TError]:
        try:
            conversation = self._repository.get_by_id(query.conversation_id)
            return GetConversationDTO.from_domain(conversation)
        except Exception as e:
            raise e

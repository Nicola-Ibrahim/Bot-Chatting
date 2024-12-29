from src.building_blocks.domain.result import Result, TError, resultify

from ....domain.conversations.interfaces.repository import AbstractConversationRepository
from ...configuration.query_handler import AbstractQueryHandler
from .get_sub_of_messages_dto import GetSubOfMessagesDTO
from .get_sub_of_messages_query import GetSubOfMessagesQuery


class GetSubOfMessagesQueryHandler(
    AbstractQueryHandler[GetSubOfMessagesQuery, Result[list[GetSubOfMessagesDTO], TError]]
):
    def __init__(self, repository: AbstractConversationRepository):
        self._repository = repository

    @resultify
    def handle(self, query: GetSubOfMessagesQuery) -> Result[list[GetSubOfMessagesDTO], TError]:
        try:
            conversation = self._repository.get_by_id(query.conversation_id)
            messages = conversation.get_messages(query.start, query.count)
            return [GetSubOfMessagesDTO.from_domain(message) for message in messages]
        except Exception as e:
            raise e

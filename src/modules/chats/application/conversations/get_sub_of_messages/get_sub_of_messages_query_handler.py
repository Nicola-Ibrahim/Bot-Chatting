from src.building_blocks.domain.result import resultify
from src.modules.chats.application.interfaces.conversation_repository import AbstractConversationRepository

from ...configuration.query.base_query_handler import BaseQueryHandler
from .get_sub_of_messages_dto import GetSubOfMessagesDTO
from .get_sub_of_messages_query import GetSubOfMessagesQuery


class GetSubOfMessagesQueryHandler(BaseQueryHandler[GetSubOfMessagesQuery, list[GetSubOfMessagesDTO]]):
    def __init__(self, repository: AbstractConversationRepository):
        self._repository = repository

    @resultify
    def handle(self, query: GetSubOfMessagesQuery) -> list[GetSubOfMessagesDTO]:
        try:
            conversation = self._repository.get_by_id(query.conversation_id)
            messages = conversation.get_messages(query.start, query.count)
            return [GetSubOfMessagesDTO.from_domain(message) for message in messages]
        except Exception as e:
            raise e
            raise e

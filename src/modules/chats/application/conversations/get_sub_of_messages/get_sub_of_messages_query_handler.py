from ....domain.conversations.interfaces.repository import Conversations
from ...configuration.query_handler import AbstractQueryHandler
from .get_sub_of_messages_dto import GetSubOfMessagesDTO
from .get_sub_of_messages_query import GetSubOfMessagesQuery


class GetSubOfMessagesQueryHandler(AbstractQueryHandler[GetSubOfMessagesQuery, list[GetSubOfMessagesDTO]]):
    def __init__(self, repository: Conversations):
        self._repository = repository

    def handle(self, query: GetSubOfMessagesQuery) -> list[GetSubOfMessagesDTO]:
        try:
            conversation = self._repository.get_by_id(query.conversation_id)
            messages = conversation.get_messages(query.start, query.count)
            return [GetSubOfMessagesDTO.from_domain(message) for message in messages]
        except Exception as e:
            raise e

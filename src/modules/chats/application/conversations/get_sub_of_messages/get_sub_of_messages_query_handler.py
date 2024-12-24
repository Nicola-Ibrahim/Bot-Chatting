from src.building_blocks.application.base_query_handler import BaseQueryHandler
from src.building_blocks.domain.result import resultify
from src.modules.chats.application.dtos.message_dto import MessageDTO
from src.modules.chats.application.interfaces.conversation_repository import AbstractConversationRepository


class GetSubOfMessagesQueryHandler(BaseQueryHandler):
    def __init__(self, repository: AbstractConversationRepository):
        self._repository = repository

    @resultify
    def handle(self, query: GetSubOfMessagesQuery) -> list[MessageDTO]:
        try:
            conversation = self._repository.get_by_id(query.conversation_id)
            messages = conversation.get_messages(query.start, query.count)
            return [MessageDTO.from_domain(message) for message in messages]
        except Exception as e:
            raise e

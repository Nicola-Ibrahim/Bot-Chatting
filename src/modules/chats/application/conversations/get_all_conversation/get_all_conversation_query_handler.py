from src.building_blocks.application.base_query_handler import BaseQueryHandler
from src.building_blocks.domain.result import resultify
from src.modules.chats.application.dtos.conversation_dto import ConversationDTO
from src.modules.chats.application.interfaces.conversation_repository import AbstractConversationRepository


class GetAllConversationsQueryHandler(BaseQueryHandler):
    def __init__(self, repository: AbstractConversationRepository):
        self._repository = repository

    @resultify
    def handle(self, query: GetAllConversationsQuery) -> list[ConversationDTO]:
        try:
            conversations = self._repository.get_all()
            return [ConversationDTO.from_domain(conversation) for conversation in conversations]
        except Exception as e:
            raise e

from src.building_blocks.application.base_query_handler import BaseQueryHandler
from src.building_blocks.domain.result import resultify
from src.modules.chats.application.dtos.conversation_dto import ConversationDTO
from src.modules.chats.application.interfaces.conversation_repository import \
    AbstractConversationRepository


class GetConversationQueryHandler(BaseQueryHandler):
    def __init__(self, repository: AbstractConversationRepository):
        self._repository = repository

    @resultify
    def handle(self, query: GetConversationQuery) -> ConversationDTO:
        try:
            conversation = self._repository.get_by_id(query.conversation_id)
            return ConversationDTO.from_domain(conversation)
        except Exception as e:
            raise e            raise e
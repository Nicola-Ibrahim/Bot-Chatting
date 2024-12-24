from uuid import UUID
from src.building_blocks.application.base_query import BaseQuery

class GetConversationQuery(BaseQuery):
    conversation_id: UUID
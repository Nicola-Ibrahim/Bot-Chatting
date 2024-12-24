from uuid import UUID
from src.building_blocks.application.base_query import BaseQuery

class GetSubOfMessagesQuery(BaseQuery):
    conversation_id: UUID
    start: int
    count: int
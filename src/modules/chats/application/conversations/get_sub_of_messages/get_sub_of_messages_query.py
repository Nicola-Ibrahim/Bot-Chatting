from uuid import UUID

from ...contracts.base_query import BaseQuery


class GetSubOfMessagesQuery(BaseQuery):
    conversation_id: UUID
    start: int
    count: int

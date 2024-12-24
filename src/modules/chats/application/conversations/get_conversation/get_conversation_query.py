from uuid import UUID

from ...contracts.base_query import BaseQuery


class GetConversationQuery(BaseQuery):
    conversation_id: UUID

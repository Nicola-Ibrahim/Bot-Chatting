from uuid import UUID

from ...contracts.query import BaseQuery


class GetConversationQuery(BaseQuery):
    conversation_id: UUID

import uuid

from src.modules.chats.application.contracts.query import BaseQuery


class GetConversationDetailsQuery(BaseQuery):
    conversation_id: uuid.UUID

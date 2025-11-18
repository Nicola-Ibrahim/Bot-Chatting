import uuid

from src.modules.chats.application.contracts.query import BaseQuery


class ListMessagesQuery(BaseQuery):
    conversation_id: uuid.UUID

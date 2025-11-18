import uuid

from src.modules.chats.application.contracts.query import BaseQuery


class ListUserConversationsQuery(BaseQuery):
    user_id: uuid.UUID

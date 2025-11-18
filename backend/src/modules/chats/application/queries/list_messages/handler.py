from __future__ import annotations

from src.modules.chats.application.configuration.query_handler import BaseQueryHandler
from src.modules.chats.application.contracts.query import BaseQuery
from src.modules.chats.application.queries.list_messages.dto import MessageDTO
from src.modules.chats.domain.messages.interfaces.repository import AbstractMessageRepository

from .query import ListMessagesQuery


class ListMessagesHandler(BaseQueryHandler):
    def __init__(self, messages_repository: AbstractMessageRepository) -> None:
        self._messages = messages_repository

    def handle(self, query: BaseQuery) -> tuple[MessageDTO, ...]:
        assert isinstance(query, ListMessagesQuery)

        messages = self._messages.list_for_conversation(str(query.conversation_id))
        result: list[MessageDTO] = []
        for message in messages:
            content = None
            if getattr(message, "contents", None):
                content = message.contents[-1]
            result.append(
                MessageDTO(
                    id=str(getattr(getattr(message, "_id", None), "value", getattr(message, "id", ""))),
                    sender_id=str(getattr(getattr(message, "_sender_id", None), "value", "")),
                    text=getattr(content, "text", None),
                    response=getattr(content, "response", None),
                    created_at=getattr(message, "_created_at", None),
                )
            )
        return tuple(result)

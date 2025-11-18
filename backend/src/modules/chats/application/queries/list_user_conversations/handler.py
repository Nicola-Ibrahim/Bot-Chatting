from __future__ import annotations

from src.modules.chats.application.configuration.query_handler import BaseQueryHandler
from src.modules.chats.application.contracts.query import BaseQuery
from src.modules.chats.application.queries.list_user_conversations.dto import ConversationSummaryDTO
from src.modules.chats.domain.interfaces.conversation_repository import BaseConversationRepository

from .query import ListUserConversationsQuery


class ListUserConversationsHandler(BaseQueryHandler):
    def __init__(self, conversation_repository: BaseConversationRepository) -> None:
        self._conversations = conversation_repository

    def handle(self, query: BaseQuery) -> tuple[ConversationSummaryDTO, ...]:
        assert isinstance(query, ListUserConversationsQuery)

        conversations = self._conversations.find_all(query.user_id)
        summaries = (
            ConversationSummaryDTO(
                id=str(conversation.id),
                title=getattr(conversation, "title", ""),
                is_archived=getattr(conversation, "is_archived", False),
            )
            for conversation in conversations
        )
        return tuple(summaries)

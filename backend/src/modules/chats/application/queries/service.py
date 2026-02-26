"""Chat Query Service."""

from __future__ import annotations

from ...domain.interfaces.conversation_repository import BaseConversationRepository
from ...domain.messages.interfaces.repository import AbstractMessageRepository
from .get_conversation_details_dto import ConversationDetailsDTO
from .get_conversation_details_query import GetConversationDetailsQuery
from .list_messages_dto import MessageDTO
from .list_messages_query import ListMessagesQuery
from .list_user_conversations_dto import ConversationSummaryDTO
from .list_user_conversations_query import ListUserConversationsQuery


class ChatQueryService:
    def __init__(
        self,
        conversation_repository: BaseConversationRepository,
        messages_repository: AbstractMessageRepository,
    ) -> None:
        self._conversations = conversation_repository
        self._messages = messages_repository

    def get_conversation_details(self, query: GetConversationDetailsQuery) -> ConversationDetailsDTO | None:
        conversation = self._conversations.find(query.conversation_id)
        if conversation is None:
            return None

        participants = []
        for participant in getattr(conversation, "participants", []):
            participant_id = getattr(participant, "id", None)
            role = getattr(participant, "_role", None)
            participants.append(
                {
                    "id": str(getattr(participant_id, "value", participant_id)),
                    "role": getattr(role, "value", str(role)) if role is not None else None,
                }
            )

        creator = getattr(conversation, "creator", None)
        creator_id = getattr(getattr(creator, "id", None), "value", None)

        return ConversationDetailsDTO(
            id=str(conversation.id),
            title=getattr(conversation, "title", ""),
            is_archived=getattr(conversation, "is_archived", False),
            creator_id=str(creator_id) if creator_id else None,
            participants=tuple(participants),
        )

    def list_messages(self, query: ListMessagesQuery) -> tuple[MessageDTO, ...]:
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

    def list_user_conversations(self, query: ListUserConversationsQuery) -> tuple[ConversationSummaryDTO, ...]:
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

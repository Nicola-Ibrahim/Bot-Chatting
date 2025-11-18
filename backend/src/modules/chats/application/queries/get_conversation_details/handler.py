from src.modules.chats.application.configuration.query_handler import BaseQueryHandler
from src.modules.chats.application.contracts.query import BaseQuery
from src.modules.chats.application.queries.get_conversation_details.dto import ConversationDetailsDTO
from src.modules.chats.domain.interfaces.conversation_repository import BaseConversationRepository

from .query import GetConversationDetailsQuery


class GetConversationDetailsHandler(BaseQueryHandler):
    def __init__(self, conversation_repository: BaseConversationRepository) -> None:
        self._conversations = conversation_repository

    def handle(self, query: BaseQuery) -> ConversationDetailsDTO | None:
        assert isinstance(query, GetConversationDetailsQuery)

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

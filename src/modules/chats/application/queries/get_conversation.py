import uuid
from dataclasses import dataclass

from src.building_blocks.domain.result import Result, resultify

from ...application.services.conversation_dto import ConversationDTO
from ..interfaces.conversation_repository import AbstractConversationRepository


@dataclass
class GetConversationByIdQuery:
    """Query to retrieve a conversation by its ID."""

    conversation_id: uuid.UUID


class GetConversationByIdQueryHandler:
    def __init__(self, repository: AbstractConversationRepository):
        self._repository = repository

    @resultify
    def handle(self, query: GetConversationByIdQuery) -> Result:
        try:
            conversation = self._repository.get_by_id(query.conversation_id)
            if not conversation:
                return Result.fail("Conversation not found.")
            return Result.ok(ConversationDTO.from_domain(conversation))
        except Exception as e:
            return str(e)

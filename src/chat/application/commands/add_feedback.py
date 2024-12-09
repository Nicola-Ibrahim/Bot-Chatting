import uuid
from dataclasses import dataclass

from ....domain.primitive.result import Result
from ...application.services.conversation_dto import ConversationDTO
from ...domain.enums.rating import RatingType
from ...domain.value_objects.feedback import Feedback
from ..interfaces.conversation_repository import AbstractConversationRepository


@dataclass
class AddFeedbackCommand:
    conversation_id: uuid.UUID
    message_id: uuid.UUID
    content_pos: int
    rating: RatingType
    comment: str


class AddFeedbackCommandHandler:
    def __init__(self, repository: AbstractConversationRepository):
        self._repository = repository

    def execute(self, dto: AddFeedbackCommand) -> Result:
        try:
            conversation = self._repository.get_by_id(dto.conversation_id)
            if not conversation:
                return Result.fail("Conversation not found.")

            feedback = Feedback.create(rating=dto.rating, comment=dto.comment)
            conversation.add_feedback_message(
                message_id=dto.message_id, content_pos=dto.content_pos, feedback=feedback
            )
            self._repository.save(conversation)
            return Result.ok(ConversationDTO.from_domain(conversation))
        except Exception as e:
            return Result.fail(str(e))

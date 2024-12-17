import uuid
from dataclasses import dataclass

from ....domain.primitive.result import Result
from ...domain.messages.rating import RatingType
from ...domain.value_objects.feedback import Feedback
from ..interfaces.conversation_repository import AbstractConversationRepository
from ..services import ConversationDTO


@dataclass
class AddFeedbackToMessageCommand:
    conversation_id: uuid.UUID
    message_id: uuid.UUID
    content_pos: int
    rating: RatingType
    comment: str


class AddFeedbackToMessageCommandHandler(BaseCommandHandler):
    def __init__(self, repository: AbstractConversationRepository):
        self._repository = repository

    def handle(self, dto: AddFeedbackCommand) -> Result:
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

from uuid import UUID

from pydantic import BaseModel

from src.building_blocks.application.base_command_handler import BaseCommandHandler
from src.building_blocks.domain.exception import BusinessRuleValidationException, RepositoryException
from src.building_blocks.domain.result import Result, resultify
from src.modules.chats.domain.messages.models.feedback import Feedback
from src.modules.chats.domain.messages.models.rating import RatingType

from ..interfaces.message_repository import AbstractMessageRepository
from ..services import messageDTO


class AddFeedbackToMessageCommand(BaseModel):
    message_id: UUID
    content_pos: int
    rating: RatingType
    comment: str

    class Config:
        schema_extra = {
            "example": {
                "message_id": "123e4567-e89b-12d3-a456-426614174000",
                "content_pos": 1,
                "rating": "positive",
                "comment": "Great message!",
            }
        }

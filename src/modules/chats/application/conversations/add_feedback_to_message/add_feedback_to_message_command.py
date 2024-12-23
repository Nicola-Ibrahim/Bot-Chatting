from uuid import UUID

from src.modules.chats.domain.messages.models.rating import RatingType

from ...contracts.base_command import BaseCommand


class AddFeedbackToMessageCommand(BaseCommand):
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

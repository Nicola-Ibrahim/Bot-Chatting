import uuid
from pydantic import BaseModel

class AddFeedbackRequest(BaseModel):
    content_pos: int
    rating: RatingType
    comment: str

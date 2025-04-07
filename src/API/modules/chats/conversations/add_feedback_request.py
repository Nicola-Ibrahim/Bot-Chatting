from pydantic import BaseModel


class AddFeedbackRequest(BaseModel):
    content_pos: int
    comment: str

from pydantic import BaseModel


class AddMessageRequest(BaseModel):
    text: str

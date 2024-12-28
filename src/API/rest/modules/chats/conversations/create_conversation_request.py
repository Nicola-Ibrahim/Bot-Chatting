from pydantic import BaseModel

class CreateConversationRequest(BaseModel):
    user_id: int

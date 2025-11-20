from pydantic import BaseModel, Field


class CreateConversationRequest(BaseModel):
    user_id: str = Field(..., description="ID of the user starting the conversation")
    user_name: str = Field(..., description="Display name of the creator")
    title: str = Field(..., description="Conversation title")

from pydantic import BaseModel


class ConversationViewModel(BaseModel):

    id: str
    name: str

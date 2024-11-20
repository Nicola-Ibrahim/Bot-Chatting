from pydantic import BaseModel


class ChatCreatedCommand(BaseModel):
    """This command is used to publish an event that chat is created"""

    id: str
    name: str

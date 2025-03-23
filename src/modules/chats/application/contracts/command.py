import uuid

from pydantic import BaseModel, Field


class BaseCommand(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)

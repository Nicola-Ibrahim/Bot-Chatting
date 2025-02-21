import uuid

from ....domain import ResponseGenerator
from ...contracts.command import BaseCommand


class GenerateResponseCommand(BaseCommand[ResponseGenerator]):
    prompt: str

    class Config:
        schema_extra = {
            "example": {
                "prompt": "What is the weather like today?",
            }
        }

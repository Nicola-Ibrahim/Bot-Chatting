from ....domain import ResponseGenerator
from ...contracts.command import BaseCommand


class GenerateResponseCommand(BaseCommand[ResponseGenerator]):
    query: str
    user_id: str

    class Config:
        schema_extra = {
            "example": {
                "query": "What is the weather like today?",
            }
        }

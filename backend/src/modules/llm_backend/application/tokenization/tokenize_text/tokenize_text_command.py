import uuid

from ....domain import Tokenizer
from ...contracts.command import BaseCommand


class TokenizeTextCommand(BaseCommand[Tokenizer]):
    text: str

    class Config:
        schema_extra = {
            "example": {
                "text": "This is an example text to be tokenized.",
            }
        }

import uuid
from dataclasses import dataclass
from typing import Optional

from .dto import BaseDTO


@dataclass
class MessageDTO(BaseDTO):
    id: uuid.UUID
    text: str
    response: Optional[str] = None
    rating: Optional[str] = None
    comment: Optional[str] = None

    @classmethod
    def from_domain(cls, domain_object):
        return cls(
            id=domain_object.id,
            text=domain_object.content.text,
            response=domain_object.content.response,
            rating=domain_object.feedback.rating.name if domain_object.feedback else None,
            comment=domain_object.feedback.comment if domain_object.feedback else None,
        )

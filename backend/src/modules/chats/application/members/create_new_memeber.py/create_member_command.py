from uuid import UUID

from pydantic import Field

from ....domain.members.root import Member
from ...contracts.command import BaseCommand


class CreateMemberCommand(BaseCommand[Member]):
    member_id: UUID
    login: str = Field(..., min_length=1, max_length=50)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    is_admin: bool = False
    is_creator: bool = False

    class Config:
        schema_extra = {
            "example": {
                "member_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "login": "johndoe",
                "first_name": "John",
                "last_name": "Doe",
                "is_admin": False,
                "is_creator": True,
            }
        }

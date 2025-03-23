from uuid import UUID

from pydantic import EmailStr, Field

from ....domain.users.root import User
from ...contracts.command import BaseCommand


class CreateUserCommand(BaseCommand):
    user_id: UUID
    name: str = Field(..., min_length=1, max_length=100)
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    raw_password: str = Field(..., min_length=6)
    phone_number: str = Field(..., min_length=10, max_length=15)
    address: str = Field(..., min_length=1, max_length=255)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "name": "John Doe",
                "username": "johndoe",
                "email": "john.doe@example.com",
                "raw_password": "securepassword123",
                "phone_number": "+1234567890",
                "address": "123 Main Street",
            }
        }

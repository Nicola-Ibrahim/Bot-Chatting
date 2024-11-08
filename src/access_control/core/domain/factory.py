import uuid

from .entity.user import Permission, Role, User
from .entity.value_object import Address, Email, Name, Password, Phone, Username


class UserDomainFactory:
    @staticmethod
    def create_user(
        username: Username,
        email: Email,
        raw_password: str,
        name: Name,
        address: Address,
        phone: Phone,
        role: Role,
        permissions: list[Permission],
    ):
        """Create a user entity in the domain"""
        hashed_password = Password.hash_password(raw_password=raw_password)
        user = User(
            id=uuid.uuid4(),
            name=name,
            username=username,
            email=email,
            password=hashed_password,
            phone=phone,
            address=address,
            permissions=permissions,
            role=role,
        )
        return user

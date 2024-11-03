from .model.entity import Permission, Role, User
from .model.value_objects import Address, Email, Name, Phone, Username


class UserFactory:
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
        hashed_password = hash_password(raw_password=raw_password)
        user = User(
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

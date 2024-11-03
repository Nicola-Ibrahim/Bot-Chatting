from uuid import UUID

from ..bounded_context.domain.model.entity import Permission, Role, User
from .user import PermissionDTO, RoleDTO, UserDTO


def map_permission_to_dto(permission: Permission) -> PermissionDTO:
    return PermissionDTO(id=str(permission.id), name=permission.name, description=permission.description)


def map_role_to_dto(role: Role) -> RoleDTO:
    return RoleDTO(
        id=str(role.id),
        name=role.name,
        description=role.description,
        permissions=[map_permission_to_dto(perm) for perm in role.permissions],
    )


def map_user_to_dto(user: User) -> UserDTO:
    return UserDTO(
        id=str(user.id),
        name={"first": user.name.first_name, "last": user.name.last_name},  # Adjust based on your Name object
        username=user.username.value,
        email=str(user.email),  # Assuming Email has a __str__ method
        phone=str(user.phone),  # Assuming Phone has a __str__ method
        address={
            "country": user.address.country,
            "city": user.address.city,
            "street": user.address.street,
            "zipcode": user.address.zipcode,
        },
        role=map_role_to_dto(user.role) if user.role else None,
        permissions=[map_permission_to_dto(p) for p in user.permissions],
    )


def map_permission_dto_to_entity(dto: PermissionDTO) -> Permission:
    return Permission(id=UUID(dto.id), name=dto.name, description=dto.description)  # Convert string back to UUID


def map_role_dto_to_entity(dto: RoleDTO) -> Role:
    return Role(
        id=UUID(dto.id),  # Convert string back to UUID
        name=dto.name,
        description=dto.description,
        permissions=[map_permission_dto_to_entity(p) for p in dto.permissions],
    )


def map_user_dto_to_entity(dto: UserDTO) -> User:
    return User(
        id=UUID(dto.id),  # Convert string back to UUID
        name=Name(first_name=dto.name["first"], last_name=dto.name["last"]),  # Create Name object
        username=Username(dto.username),
        email=Email.from_text(dto.email),
        phone=Phone(country_code=dto.phone[:3], number=int(dto.phone[3:])),  # Example parsing
        address=Address(**dto.address),  # Assuming address fields are correctly named
        role=map_role_dto_to_entity(dto.role) if dto.role else None,
        permissions=[map_permission_dto_to_entity(perm) for perm in dto.permissions],
    )

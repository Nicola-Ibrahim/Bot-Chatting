from dataclasses import dataclass, field

from src.building_blocks.domain.entity import Entity

from .permission import Permission


@dataclass
class Role(Entity):
    name: str
    description: str | None = None
    permissions: list[Permission] = field(default_factory=list)

    def __post_init__(self):
        if not self.name:
            raise ValueError("Role name must be provided.")
        if len(self.name) < 3 or len(self.name) > 50:
            raise ValueError("Role name must be between 3 and 50 characters.")
        if not self.name.isalnum():
            raise ValueError("Role name must contain only alphanumeric characters.")
        if self.description and len(self.description) > 200:
            raise ValueError("Role description must not exceed 200 characters.")

    def add_permission(self, permission: Permission):
        if permission not in self.permissions:
            self.permissions.append(permission)
        else:
            raise ValueError(f"Permission '{permission.name}' is already assigned to the role.")

    def remove_permission(self, permission: Permission):
        if permission in self.permissions:
            self.permissions.remove(permission)
        else:
            raise ValueError(f"Permission '{permission.name}' is not assigned to the role.")

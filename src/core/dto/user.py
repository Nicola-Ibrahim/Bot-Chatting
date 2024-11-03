import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class PermissionDTO:
    id: str  # Assuming UUID is serialized as a string
    name: str
    description: Optional[str] = None


@dataclasses.dataclass
class RoleDTO:
    id: str  # Assuming UUID is serialized as a string
    name: str
    description: Optional[str] = None
    permissions: List[PermissionDTO] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class UserDTO:
    id: str  # Assuming UUID is serialized as a string
    name: dict  # Could be a dict with first and last names, etc.
    username: str
    email: str
    phone: str
    address: dict  # Could be a dict with address fields
    role: Optional[RoleDTO] = None
    permissions: List[PermissionDTO] = dataclasses.field(default_factory=list)

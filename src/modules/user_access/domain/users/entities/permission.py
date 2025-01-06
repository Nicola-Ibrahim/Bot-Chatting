import dataclasses
from typing import Optional

from src.building_blocks.domain.entity import Entity


@dataclasses.dataclass
class Permission(Entity):
    name: str
    description: Optional[str] = None

    def __post_init__(self):
        if not self.name:
            raise ValueError("Permission name must be provided.")
        if len(self.name) < 3 or len(self.name) > 50:
            raise ValueError("Permission name must be between 3 and 50 characters.")
        if not self.name.isalnum():
            raise ValueError("Permission name must contain only alphanumeric characters.")
        if self.description and len(self.description) > 200:
            raise ValueError("Permission description must not exceed 200 characters.")

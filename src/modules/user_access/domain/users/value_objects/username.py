import re
from dataclasses import dataclass

from src.building_blocks.domain.value_object import ValueObject


@dataclass(frozen=True)
class Username(ValueObject):
    value: str

    def __post_init__(self):
        if len(self.value) < 3 or len(self.value) > 20:
            raise ValueError("Username must be between 3 and 20 characters.")
        if not re.match("^[a-zA-Z0-9_.-]+$", self.value):
            raise ValueError("Username can only contain letters, numbers, dots, hyphens, and underscores.")

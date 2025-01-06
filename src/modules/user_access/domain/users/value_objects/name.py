from dataclasses import dataclass

from src.building_blocks.domain.value_object import ValueObject


@dataclass(frozen=True)
class Name(ValueObject):
    first_name: str
    last_name: str
    middle_name: str = ""

    def __post_init__(self):
        for name in (self.first_name, self.last_name, self.middle_name):
            if name and (not name.isalpha() or len(name) < 1 or len(name) > 50):
                raise ValueError(
                    "Names can only contain alphabetic characters and must be between 1 and 50 characters."
                )

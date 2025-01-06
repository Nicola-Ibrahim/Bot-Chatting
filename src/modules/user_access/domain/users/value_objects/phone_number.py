from dataclasses import dataclass

from src.building_blocks.domain.value_object import ValueObject


@dataclass(frozen=True)
class PhoneNumber(ValueObject):
    country_code: str
    number: int

    def __post_init__(self):
        if not self.country_code.startswith("+") or not self.country_code[1:].isdigit():
            raise ValueError("Country code must start with '+' followed by digits.")
        if not (1 <= len(self.country_code) <= 4):
            raise ValueError("Country code must be between 1 and 4 digits.")
        if not (1000000000 <= self.number <= 9999999999):
            raise ValueError("Phone number must be 10 digits long.")

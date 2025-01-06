from dataclasses import dataclass

from src.building_blocks.domain.value_object import ValueObject


@dataclass(frozen=True)
class Address(ValueObject):
    country: str
    city: str
    street: str
    zipcode: str

    def __post_init__(self):
        if not (self.country and self.city and self.street):
            raise ValueError("Country, city, and street cannot be empty.")
        if not self.zipcode.isdigit() or len(self.zipcode) not in [5, 9]:
            raise ValueError("Zip code must be either 5 or 9 digits long and numeric.")

import dataclasses
import hashlib
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Password:
    _value: str

    def __post_init__(self):
        if not self.is_valid(self._value):
            raise ValueError("Password does not meet the required criteria.")

        # Setting the hashed password as the _hashed_value attribute
        object.__setattr__(self, "_hashed_value", self.hash_password(self._value))

    @staticmethod
    def is_valid(password: str) -> bool:
        """Check if the password meets specific security criteria."""
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):  # At least one uppercase letter
            return False
        if not re.search(r"[a-z]", password):  # At least one lowercase letter
            return False
        if not re.search(r"\d", password):  # At least one digit
            return False
        if not re.search(r"[@$!%*?&]", password):  # At least one special character
            return False
        return True

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash the password using a secure hashing algorithm."""
        # Using SHA-256 here; in production, use bcrypt or similar for added security
        return hashlib.sha256(password.encode()).hexdigest()

    def verify(self, plain_password: str) -> bool:
        """Verify if a plain password matches the stored hashed password."""
        return self._hashed_value == self.hash_password(plain_password)

    @property
    def hashed_value(self) -> str:
        """Retrieve the hashed password (to be stored in the database)."""
        return self._hashed_value


@dataclasses.dataclass(frozen=True)
class Name:
    first_name: str
    last_name: str
    middle_name: str = ""

    def __post_init__(self):
        for name in (self.first_name, self.last_name, self.middle_name):
            if name and (not name.isalpha() or len(name) < 1 or len(name) > 50):
                raise ValueError(
                    "Names can only contain alphabetic characters and must be between 1 and 50 characters."
                )


@dataclasses.dataclass(frozen=True)
class Username:
    value: str

    def __post_init__(self):
        if len(self.value) < 3 or len(self.value) > 20:
            raise ValueError("Username must be between 3 and 20 characters.")
        if not re.match("^[a-zA-Z0-9_.-]+$", self.value):
            raise ValueError("Username can only contain letters, numbers, dots, hyphens, and underscores.")


@dataclasses.dataclass(frozen=True)
class Email:
    local_part: str
    domain_part: str

    @classmethod
    def from_text(cls, address: str):
        if "@" not in address:
            raise ValueError("Email address must contain '@'")
        local_part, _, domain_part = address.partition("@")
        return cls(local_part, domain_part)

    def __post_init__(self):
        if not self.local_part or not self.domain_part:
            raise ValueError("Email must have both local and domain parts.")
        if not re.match(r"^[a-zA-Z0-9_.+-]+$", self.local_part):
            raise ValueError("Invalid characters in local part of the email.")
        if not re.match(r"^[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$", self.domain_part):
            raise ValueError("Invalid domain format.")
        object.__setattr__(self, "_parts", (self.local_part, self.domain_part))

    def __str__(self) -> str:
        return "@".join(self._parts)


@dataclasses.dataclass(frozen=True)
class Phone:
    country_code: str
    number: int

    def __post_init__(self):
        if not self.country_code.startswith("+") or not self.country_code[1:].isdigit():
            raise ValueError("Country code must start with '+' followed by digits.")
        if not (1 <= len(self.country_code) <= 4):
            raise ValueError("Country code must be between 1 and 4 digits.")
        if not (1000000000 <= self.number <= 9999999999):
            raise ValueError("Phone number must be 10 digits long.")


@dataclasses.dataclass(frozen=True)
class Address:
    country: str
    city: str
    street: str
    zipcode: str

    def __post_init__(self):
        if not (self.country and self.city and self.street):
            raise ValueError("Country, city, and street cannot be empty.")
        if not self.zipcode.isdigit() or len(self.zipcode) not in [5, 9]:
            raise ValueError("Zip code must be either 5 or 9 digits long and numeric.")

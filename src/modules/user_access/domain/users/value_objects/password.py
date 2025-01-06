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
    def hash_password(raw_password: str) -> str:
        """Hash the password using a secure hashing algorithm."""
        # Using SHA-256 here; in production, use bcrypt or similar for added security
        return hashlib.sha256(raw_password.encode()).hexdigest()

    def verify(self, raw_password: str) -> bool:
        """Verify if a plain password matches the stored hashed password."""
        return self._hashed_value == self.hash_password(raw_password)

    @property
    def hashed_value(self) -> str:
        """Retrieve the hashed password (to be stored in the database)."""
        return self._hashed_value

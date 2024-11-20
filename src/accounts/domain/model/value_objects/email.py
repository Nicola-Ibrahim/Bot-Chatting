import dataclasses
import re


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

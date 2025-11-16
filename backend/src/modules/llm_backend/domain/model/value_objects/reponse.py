from dataclasses import dataclass


@dataclass(frozen=True)
class Response:
    value: str
    MAX_LENGTH = 5000

    def __post_init__(self):
        if not self.value.strip():
            raise ValueError("Response text cannot be empty")
        if len(self.value) > self.MAX_LENGTH:
            raise ValueError(f"Response text exceeds {self.MAX_LENGTH} characters")

from dataclasses import dataclass


@dataclass(frozen=True)
class Query:
    value: str
    MAX_LENGTH = 2000

    def __post_init__(self):
        if not self.value.strip():
            raise ValueError("Input text cannot be empty")
        if len(self.value) > self.MAX_LENGTH:
            raise ValueError(f"Input text exceeds {self.MAX_LENGTH} characters")

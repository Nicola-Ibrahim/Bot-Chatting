from dataclasses import dataclass, field
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from src.building_blocks.domain.entity import AggregateRoot


@dataclass
class Token(AggregateRoot):
    """
    Represents an API token for accessing models.
    """

    id: UUID
    user_id: UUID
    token: str
    rate_limit: int  # Requests per minute
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=30))

    def is_valid(self) -> bool:
        """
        Checks if the token is valid (not expired).

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        return datetime.now(timezone.utc) < self.expires_at

    def can_make_request(self) -> bool:
        """
        Checks if the token can make a request based on rate limits.

        Returns:
            bool: True if the token can make a request, False otherwise.
        """
        # Implement rate limiting logic here
        return True

from abc import ABC, abstractmethod
from .root import Token


class TokenRepository(ABC):
    @abstractmethod
    def get_token(self, id: str) -> Token:
        pass

    @abstractmethod
    def save_token(self, token: Token) -> None:
        pass

    # ...other repository methods...

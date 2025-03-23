from abc import ABC, abstractmethod
from typing import Any

from ..contracts.command import BaseCommand


class BaseCommandHandler(ABC):
    @abstractmethod
    def handle(self, command: BaseCommand) -> Any:
        pass

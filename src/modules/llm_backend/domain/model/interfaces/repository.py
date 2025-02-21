from abc import ABC, abstractmethod

from ..events import Model


class ModelRepository(ABC):
    @abstractmethod
    def get_model(self, id: str) -> Model:
        pass

    @abstractmethod
    def save_model(self, model: Model) -> None:
        pass

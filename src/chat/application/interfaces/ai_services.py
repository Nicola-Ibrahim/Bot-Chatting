from abc import ABC, abstractmethod


class AbstractResponseGeneratorService(ABC):
    @abstractmethod
    def generate_answer(self, text: str) -> str:
        """Generate an answer for the given message"""


class AbstractTokenizerService(ABC):
    @abstractmethod
    def tokenize(self, text):
        """tokenize the text"""

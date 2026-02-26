"""Tokenization Service."""

from ...domain import Tokenizer, Tokens
from .tokenize_text_command import TokenizeTextCommand


class TokenizationService:
    def __init__(self, repository: Tokens):
        self._repository = repository

    def tokenize(self, command: TokenizeTextCommand) -> str:
        tokens = Tokenizer.tokenize(text=command.text)
        self._repository.save(tokens)
        return tokens.id

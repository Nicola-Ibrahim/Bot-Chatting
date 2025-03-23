from ....domain import Tokenizer, Tokens
from ...configuration.command_handler import BaseCommandHandler
from .tokenize_text_command import TokenizeTextCommand


class TokenizeTextCommandHandler(BaseCommandHandler[TokenizeTextCommand, str]):
    def __init__(self, repository: Tokens):
        self._repository = repository

    def handle(self, command: TokenizeTextCommand) -> str:
        tokens = Tokenizer.tokenize(text=command.text)
        self._repository.save(tokens)
        return tokens.id

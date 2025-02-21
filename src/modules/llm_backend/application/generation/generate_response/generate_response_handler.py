from ....domain import ResponseGenerator, Responses
from ...configuration.command_handler import AbstractCommandHandler
from .generate_response_command import GenerateResponseCommand


class GenerateResponseCommandHandler(AbstractCommandHandler[GenerateResponseCommand, str]):
    def __init__(self, repository: Responses):
        self._repository = repository

    def handle(self, command: GenerateResponseCommand) -> str:
        response = ResponseGenerator.generate(
            prompt=command.prompt
        )
        self._repository.save(response)
        return response.id

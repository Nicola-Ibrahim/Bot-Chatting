from ....domain import ResponseGenerator, Responses
from ....domain.model.root import ModelInteraction
from ...configuration.command_handler import AbstractCommandHandler
from .generate_response_command import GenerateResponseCommand

from ..pipelines
class GenerateResponseCommandHandler(AbstractCommandHandler[GenerateResponseCommand, str]):
    def __init__(self, repository: Responses):
        self._repository = repository

    def handle(self, command: GenerateResponseCommand) -> str:
        response = LLMQueryProcessingPipeline().process(command.query)

        model_interaction = ModelInteraction.create(
            model_name=command.model_name,
            user_id=command.user_id,
            input_text=command.query,
            response_text=response,
        )

        self._repository.save(model_interaction)
        return model_interaction.id

"""Generation Service."""

from ...domain import Responses
from ...domain.model.root import ModelInteraction
from .generate_response_command import GenerateResponseCommand
from .pipelines.pipeline import LLMQueryProcessingPipeline


class GenerationService:
    def __init__(self, repository: Responses):
        self._repository = repository

    def generate(self, command: GenerateResponseCommand) -> str:
        # Note: Preserving original logic including unimported LLMQueryProcessingPipeline
        response = LLMQueryProcessingPipeline().process(command.query)

        model_interaction = ModelInteraction.create(
            model_name=command.model_name,
            user_id=command.user_id,
            input_text=command.query,
            response_text=response,
        )

        self._repository.save(model_interaction)
        return model_interaction.id

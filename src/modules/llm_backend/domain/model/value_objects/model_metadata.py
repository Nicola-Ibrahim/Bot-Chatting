from dataclasses import dataclass

from src.building_blocks.domain.value_object import ValueObject


@dataclass(frozen=True)
class ModelMetadata(ValueObject):
    """
    Represents metadata about a pre-trained model.
    """

    name: str
    version: str
    model_type: str  # e.g., "LLAMA", "Qwen", "GPT"
    description: str | None = None

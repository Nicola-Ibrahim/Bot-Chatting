from abc import ABC, abstractmethod
from typing import Any, Dict, List


class PipelineStage(ABC):
    """Abstract base class for a pipeline stage, defining the interface for all stages."""

    @abstractmethod
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processes the input data and returns the result.

        Args:
            data (Dict[str, Any]): The input data dictionary that contains the information needed for processing.

        Returns:
            Dict[str, Any]: The output data dictionary with the results of the processing.
        """
        raise NotImplementedError("Subclasses must implement the 'process' method.")


class Pipeline:
    """Pipeline class that manages and runs a sequence of stages."""

    def __init__(self, stages: List[PipelineStage]) -> None:
        """Initializes the Pipeline with a list of processing stages.

        Args:
            stages (List[PipelineStage]): A list of PipelineStage instances that define the pipeline.
        """
        self.stages = stages

    def run(self, initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executes the pipeline, passing data through each stage sequentially.

        Args:
            initial_data (Dict[str, Any]): The initial data dictionary to be processed by the pipeline.

        Returns:
            Dict[str, Any]: The final output after all stages have processed the data.
        """
        data = initial_data
        for stage in self.stages:
            # Collect stage output, and update the data dictionary accordingly.
            stage_output = stage.process(data)
            if not isinstance(stage_output, dict):
                raise TypeError(f"Stage output must be a dictionary, got {type(stage_output)} instead.")

            # Use a temporary variable to handle updates cleanly.
            updated_data = data.copy()
            updated_data.update(stage_output)
            data = updated_data

        return data

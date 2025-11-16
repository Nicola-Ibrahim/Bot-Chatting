from abc import ABC, abstractmethod
from typing import Any


class PipelineExecutionError(Exception):
    """Base exception for pipeline processing failures"""

    def __init__(self, stage: str, message: str):
        super().__init__(f"[{stage}] {message}")
        self.stage = stage
        self.message = message


class PipelineStage(ABC):
    """Abstract base class for a pipeline stage, defining the interface for all stages."""

    @abstractmethod
    def process(self, data: dict[str, Any]) -> dict[str, Any]:
        """Processes the input data and returns the result.

        Args:
            data (dict[str, Any]): The input data dictionary that contains the information needed for processing.

        Returns:
            dict[str, Any]: The output data dictionary with the results of the processing.
        """
        raise NotImplementedError("Subclasses must implement the 'process' method.")


class Pipeline:
    """Pipeline class that manages and runs a sequence of stages."""

    def __init__(self, stages: list[PipelineStage]) -> None:
        """Initializes the Pipeline with a list of processing stages.

        Args:
            stages (list[PipelineStage]): A list of PipelineStage instances that define the pipeline.
        """
        self.stages = stages

    def validate(self) -> bool:
        """Validates the pipeline by checking that all stages are properly initialized.

        Returns:
            bool: True if the pipeline is valid, False otherwise.
        """
        if not self.stages:
            return False

        for stage in self.stages:
            if not isinstance(stage, PipelineStage):
                return False

        return True

    def run(self, initial_data: dict[str, Any]) -> dict[str, Any]:
        """Executes the pipeline, passing data through each stage sequentially.

        Args:
            initial_data (dict[str, Any]): The initial data dictionary to be processed by the pipeline.

        Returns:
            dict[str, Any]: The final output after all stages have processed the data.

        Raises:
            RuntimeError: If the pipeline is not valid or a stage fails to process the data.
        """
        if not self.validate():
            raise RuntimeError("Pipeline validation failed.")

        data = initial_data.copy()  # Treat data as immutable

        for stage in self.stages:
            try:
                stage_output = stage.process(data)

                if not isinstance(stage_output, dict):
                    raise TypeError(f"Stage output must be a dictionary, got {type(stage_output)} instead.")

                # Update data with stage output
                data.update(stage_output)
            except Exception as e:
                raise RuntimeError(f"Pipeline execution failed at stage {stage.__class__.__name__}: {e}")

        return data

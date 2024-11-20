from abc import ABC, abstractmethod


class AbstractFeedbackRepository(ABC):
    """
    Abstract base class for managing feedbacks.
    """

    @abstractmethod
    def add_feedback(self, feedback: dict):
        """
        Adds a feedbacks entry.
        :param feedback: Dictionary representing the feedbacks details.
        """
        pass

    @abstractmethod
    def get_feedback(self):
        """
        Retrieves all feedbacks entries.
        :return: List of feedbacks entries.
        """
        pass

    @abstractmethod
    def delete_feedback(self, feedback_id: int):
        """
        Deletes a feedbacks entry by its ID.
        :param feedback_id: The ID of the feedbacks to delete.
        """
        pass

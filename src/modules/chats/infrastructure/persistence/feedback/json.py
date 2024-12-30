import json
import os

from chat.application.interface.feedback_repository import AbstractFeedbackRepository
from common.infra.config import FEEDBACK_DIR


class JsonFileFeedbackRepository(AbstractFeedbackRepository):
    """
    A feedbacks manager that stores feedbacks in a file.
    """

    def __init__(self, file_name: str):
        self.file_path = os.path.join(FEEDBACK_DIR, file_name)
        # Ensure the feedbacks file exists
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                json.dump([], file)  # Initialize an empty list in the file

    def _read_feedbacks(self):
        """
        Internal method to read feedbacks from the file.
        """
        with open(self.file_path, "r") as file:
            return json.load(file)

    def _write_feedbacks(self, feedbacks):
        """
        Internal method to write feedbacks to the file.
        """
        with open(self.file_path, "w") as file:
            json.dump(feedbacks, file, indent=4)

    def add_feedback(self, feedback: dict):
        """
        Adds a feedbacks to the file.
        :param feedback: Dictionary representing the feedbacks.
        """
        feedbacks = self._read_feedbacks()
        feedback_id = len(feedbacks) + 1
        feedback["id"] = feedback_id  # Assign a unique ID to the feedbacks
        feedbacks.append(feedback)
        self._write_feedbacks(feedbacks)
        print(f"Feedback added with ID {feedback_id}")
        return feedback_id

    def get_feedback(self):
        """
        Retrieves all feedbacks entries from the file.
        :return: List of feedbacks entries.
        """
        return self._read_feedbacks()

    def delete_feedback(self, feedback_id: int):
        """
        Deletes a feedbacks entry by ID.
        :param feedback_id: The ID of the feedbacks to delete.
        """
        feedbacks = self._read_feedbacks()
        feedbacks = [fb for fb in feedbacks if fb["id"] != feedback_id]
        self._write_feedbacks(feedbacks)
        print(f"Feedback with ID {feedback_id} has been deleted.")

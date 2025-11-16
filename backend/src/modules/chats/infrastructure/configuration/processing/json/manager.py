import json
import os


class JsonFileManager:
    """
    Handles low-level JSON file operations.
    """

    DEFAULT_PREFIX = "chat_"

    def __init__(self, directory: str, prefix: str = None):
        """
        Initializes the JsonFileManager.

        Args:
            directory (str): The base directory for storing JSON files.
        """
        self.prefix = prefix or self.DEFAULT_PREFIX
        self.directory = directory
        self._ensure_directory_exists()

    def _ensure_directory_exists(self) -> None:
        """
        Ensures the base directory exists by creating it if necessary.
        """
        os.makedirs(self.directory, exist_ok=True)

    def _get_file_path(self, file_id: str) -> str:
        """
        Constructs the full file path for a given file ID.

        Args:
            file_id (str): The unique identifier for the file (without prefix or extension).

        Returns:
            str: The full file path for the JSON file.
        """
        return os.path.join(self.directory, f"{self.prefix}{file_id}.json")

    def file_exists(self, file_id: str) -> bool:
        """
        Checks if a file exists for the given file ID.

        Args:
            file_id (str): The unique identifier for the file.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        return os.path.exists(self._get_file_path(file_id))

    def read(self, file_id: str) -> dict:
        """
        Reads JSON data from a file.

        Args:
            file_id (str): The unique identifier for the file.

        Returns:
            dict: The parsed JSON data.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file content is not valid JSON.
        """
        if not self.file_exists(file_id):
            raise FileNotFoundError(f"File with ID '{file_id}' not found.")

        file_path = self._get_file_path(file_id)
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in file '{file_path}': {e}")

    def write(self, file_id: str, data: dict) -> None:
        """
        Writes JSON data to a file.

        Args:
            file_id (str): The unique identifier for the file.
            data (dict): The data to write to the file.
        """
        file_path = self._get_file_path(file_id)
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def delete(self, file_id: str) -> None:
        """
        Deletes a JSON file.

        Args:
            file_id (str): The unique identifier for the file.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        if not self.file_exists(file_id):
            raise FileNotFoundError(f"File with ID '{file_id}' not found.")

        os.remove(self._get_file_path(file_id))

    def list_files(self) -> list[str]:
        """
        Lists all file IDs with the current prefix in the directory.

        Returns:
            list[str]: A list of file IDs (without prefix or extension).
        """
        return [
            filename[len(self.prefix) : -len(".json")]
            for filename in os.listdir(self.directory)
            if filename.startswith(self.prefix) and filename.endswith(".json")
        ]

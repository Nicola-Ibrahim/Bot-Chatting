from src.building_blocks.domain.exception import BusinessRuleValidationException
from src.modules.chats.infrastructure.domain.exceptions import RepositoryException

from ....domain.conversations.interfaces.downloader import AbstractConversationDownloader
from ....domain.conversations.interfaces.repository import Conversations
from ...configuration.command_handler import AbstractCommandHandler
from .download_conversation_command import DownloadConversationCommand


class DownloadConversationCommandHandler(AbstractCommandHandler[DownloadConversationCommand, None]):
    def __init__(self, conversation_downloader: AbstractConversationDownloader, repository: Conversations):
        self._conversation_downloader = conversation_downloader
        self._repository = repository

    def handle(self, command: DownloadConversationCommand) -> None:
        try:
            conversation = self._repository.get_by_id(command.conversation_id)

            downloaded_data = self._conversation_downloader.download(conversation)

            return downloaded_data

        except (BusinessRuleValidationException, RepositoryException) as e:
            raise e

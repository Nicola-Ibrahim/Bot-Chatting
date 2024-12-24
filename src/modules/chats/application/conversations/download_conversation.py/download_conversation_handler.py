from src.building_blocks.domain.exception import BusinessRuleValidationException
from src.building_blocks.domain.result import Result, resultify
from src.modules.chats.application.interfaces.conversation_repository import AbstractConversationRepository
from src.modules.chats.application.interfaces.downloader import AbstractConversationDownloader
from src.modules.chats.infra.persistence.exceptions import RepositoryException

from ...configuration.command.base_command_handler import BaseCommandHandler
from .download_conversation_command import DownloadConversationCommand


class DownloadConversationCommandHandler(BaseCommandHandler[DownloadConversationCommand]):
    def __init__(
        self, conversation_downloader: AbstractConversationDownloader, repository: AbstractConversationRepository
    ):
        self._conversation_downloader = conversation_downloader
        self._repository = repository

    @resultify
    def handle(self, command: DownloadConversationCommand) -> Result:
        try:
            conversation = self._repository.get_by_id(command.conversation_id)

            downloaded_data = self._conversation_downloader.download(conversation)

            return downloaded_data

        except (BusinessRuleValidationException, RepositoryException) as e:
            return e

from src.building_blocks.domain.exception import BusinessRuleValidationException
from src.building_blocks.domain.result import Result, TError, resultify
from src.modules.chats.infra.domain.exceptions import RepositoryException

from ....domain.conversations.interfaces.downloader import AbstractConversationDownloader
from ....domain.conversations.interfaces.repository import AbstractConversationRepository
from ...configuration.command_handler import AbstractCommandHandler
from .download_conversation_command import DownloadConversationCommand


class DownloadConversationCommandHandler(AbstractCommandHandler[DownloadConversationCommand, Result[None, TError]]):
    def __init__(
        self, conversation_downloader: AbstractConversationDownloader, repository: AbstractConversationRepository
    ):
        self._conversation_downloader = conversation_downloader
        self._repository = repository

    @resultify
    def handle(self, command: DownloadConversationCommand) -> Result[None, TError]:
        try:
            conversation = self._repository.get_by_id(command.conversation_id)

            downloaded_data = self._conversation_downloader.download(conversation)

            return downloaded_data

        except (BusinessRuleValidationException, RepositoryException) as e:
            return e

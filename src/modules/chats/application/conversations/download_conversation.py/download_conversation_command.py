from uuid import UUID

from src.building_blocks.domain.exception import BusinessRuleValidationException
from src.building_blocks.domain.result import Result, resultify
from src.modules.chats.application.dtos.conversation_dto import ConversationDTO
from src.modules.chats.application.interfaces.conversation_repository import AbstractConversationRepository
from src.modules.chats.application.interfaces.downloader import AbstractConversationDownloader
from src.modules.chats.infra.persistence.exceptions import RepositoryException

from ..contracts.command_base import CommandBase


class DownloadConversationCommand(CommandBase[Result[ConversationDTO, str]]):
    conversation_id: UUID

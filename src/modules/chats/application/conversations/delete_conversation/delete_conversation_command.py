import uuid

from pydantic import BaseModel

from src.building_blocks.application.base_command_handler import BaseCommandHandler
from src.building_blocks.domain.exception import BusinessRuleValidationException, RepositoryException
from src.building_blocks.domain.result import Result, resultify

from ....domain.interfaces.conversation_repository import AbstractConversationRepository
from ..contracts.command_base import CommandBase


class DeleteConversationCommand(BaseModel, CommandBase[Result[None, str]]):
    conversation_id: uuid.UUID

    class Config:
        schema_extra = {"example": {"conversation_id": "123e4567-e89b-12d3-a456-426614174000"}}
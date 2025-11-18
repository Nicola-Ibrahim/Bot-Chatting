from __future__ import annotations

from src.modules.chats.application.conversation_lifecycle.start_conversation.dto import ConversationStartedDTO
from src.modules.chats.application.contracts.command import BaseCommand
from src.modules.chats.application.configuration.command_handler import BaseCommandHandler
from src.modules.chats.domain.conversations.conversation import Conversation
from src.modules.chats.domain.members.value_objects.member_id import MemberId
from src.modules.chats.domain.interfaces.conversation_repository import BaseConversationRepository

from .command import StartConversationCommand


class StartConversationHandler(BaseCommandHandler):
    def __init__(self, conversation_repository: BaseConversationRepository) -> None:
        self._conversations = conversation_repository

    def handle(self, command: BaseCommand) -> ConversationStartedDTO:
        assert isinstance(command, StartConversationCommand)

        creator_id = MemberId.create(command.user_id)
        conversation = Conversation.create(creator_id=creator_id, creator_name=command.user_name, title=command.title)
        self._conversations.save(conversation)
        return ConversationStartedDTO(conversation_id=str(conversation.id), title=conversation.title)

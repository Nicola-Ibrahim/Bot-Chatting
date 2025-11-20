import logging
from typing import Any, Callable, Type

from src.database.session import SQLAlchemySessionFactory
from src.modules.chats.application.conversation_lifecycle.archive_conversation.command import (
    ArchiveConversationCommand,
)
from src.modules.chats.application.conversation_lifecycle.archive_conversation.handler import (
    ArchiveConversationHandler,
)
from src.modules.chats.application.conversation_lifecycle.rename_conversation.command import (
    RenameConversationCommand,
)
from src.modules.chats.application.conversation_lifecycle.rename_conversation.handler import (
    RenameConversationHandler,
)
from src.modules.chats.application.conversation_lifecycle.start_conversation.command import (
    StartConversationCommand,
)
from src.modules.chats.application.conversation_lifecycle.start_conversation.handler import (
    StartConversationHandler,
)
from src.modules.chats.application.membership.add_member.command import AddMemberCommand
from src.modules.chats.application.membership.add_member.handler import AddMemberHandler
from src.modules.chats.application.membership.change_member_role.command import ChangeMemberRoleCommand
from src.modules.chats.application.membership.change_member_role.handler import ChangeMemberRoleHandler
from src.modules.chats.application.membership.remove_member.command import RemoveMemberCommand
from src.modules.chats.application.membership.remove_member.handler import RemoveMemberHandler
from src.modules.chats.application.messaging.delete_message.command import DeleteMessageCommand
from src.modules.chats.application.messaging.delete_message.handler import DeleteMessageHandler
from src.modules.chats.application.messaging.edit_message.command import EditMessageCommand
from src.modules.chats.application.messaging.edit_message.handler import EditMessageHandler
from src.modules.chats.application.messaging.send_message.command import SendMessageCommand
from src.modules.chats.application.messaging.send_message.handler import SendMessageHandler
from src.modules.chats.application.queries.get_conversation_details.handler import GetConversationDetailsHandler
from src.modules.chats.application.queries.get_conversation_details.query import GetConversationDetailsQuery
from src.modules.chats.application.queries.list_messages.handler import ListMessagesHandler
from src.modules.chats.application.queries.list_messages.query import ListMessagesQuery
from src.modules.chats.application.queries.list_user_conversations.handler import ListUserConversationsHandler
from src.modules.chats.application.queries.list_user_conversations.query import ListUserConversationsQuery
from src.modules.chats.domain.messages.interfaces.response_generator import ResponseGenerator

from .containers import ChatDIContainer

log = logging.getLogger(__name__)


class _EchoResponseGenerator(ResponseGenerator):
    """Simple fallback response generator when none is configured."""

    def generate_answer(self, text: str) -> str:
        return text


def _get_response_generator(container: ChatDIContainer) -> ResponseGenerator:
    provider = getattr(container, "response_generator", None)
    if provider:
        try:
            return provider()
        except Exception:
            log.exception("Unable to resolve configured response generator, falling back to echo generator.")
    return _EchoResponseGenerator()


HANDLER_REGISTRY: dict[Type[Any], Callable[[ChatDIContainer], object]] = {
    # Conversation lifecycle
    StartConversationCommand: lambda c: StartConversationHandler(c.repository.conversation_repository()),
    RenameConversationCommand: lambda c: RenameConversationHandler(c.repository.conversation_repository()),
    ArchiveConversationCommand: lambda c: ArchiveConversationHandler(c.repository.conversation_repository()),
    # Membership
    AddMemberCommand: lambda c: AddMemberHandler(c.repository.conversation_repository()),
    ChangeMemberRoleCommand: lambda c: ChangeMemberRoleHandler(c.repository.conversation_repository()),
    RemoveMemberCommand: lambda c: RemoveMemberHandler(c.repository.conversation_repository()),
    # Messaging
    SendMessageCommand: lambda c: SendMessageHandler(
        messages_repository=c.repository.message_repository(),
        response_generator=_get_response_generator(c),
    ),
    EditMessageCommand: lambda c: EditMessageHandler(
        messages_repository=c.repository.message_repository(),
        response_generator=_get_response_generator(c),
    ),
    DeleteMessageCommand: lambda c: DeleteMessageHandler(c.repository.message_repository()),
    # Queries
    GetConversationDetailsQuery: lambda c: GetConversationDetailsHandler(c.repository.conversation_repository()),
    ListMessagesQuery: lambda c: ListMessagesHandler(c.repository.message_repository()),
    ListUserConversationsQuery: lambda c: ListUserConversationsHandler(c.repository.conversation_repository()),
}


class ChatsStartUp:
    """Composition root for Chats bounded context (self-owned DI container)."""

    def __init__(self) -> None:
        self._container: ChatDIContainer | None = None

    @property
    def container(self) -> ChatDIContainer:
        if self._container is None:
            raise RuntimeError("Chats container not initialized")
        return self._container

    def initialize(
        self,
        *,
        database_url: str,
        max_active_chats_per_user: int,
    ) -> "ChatsStartUp":
        """Create container, load config dict, init resources, wire."""
        if not database_url:
            raise ValueError("Chats configuration requires a 'database_url'")

        config = {
            "max_active_chats_per_user": max_active_chats_per_user,
        }

        try:
            self._session_factory = SQLAlchemySessionFactory.acquire(database_url)
            self._container = ChatDIContainer(config=config, session_factory=self._session_factory)
            # expected: {"database": {"url": "..."}}

            # Order: init resources, then wire packages using Provide[...] markers
            self._container.init_resources()

            # Build mediator and register all command/query handlers
            mediator = self._container.mediator()
            for message_type, handler_factory in HANDLER_REGISTRY.items():
                handler = handler_factory(self._container)
                mediator.register(message_type, handler)

            return self
        except Exception as ex:
            raise RuntimeError("Chats module bootstrap failed") from ex

    def stop(self) -> None:
        """Graceful shutdown."""
        try:
            if self._container:
                self._container.shutdown_resources()
                self._container.unwire()
        finally:
            SQLAlchemySessionFactory.release(self._database_url)
            self._container = None

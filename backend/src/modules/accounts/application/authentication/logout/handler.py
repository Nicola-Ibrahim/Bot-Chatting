"""Handler that revokes a session."""

from __future__ import annotations

import uuid

from src.modules.accounts.domain.aggregates.session.value_objects.session_id import SessionId
from src.modules.accounts.domain.interfaces.session_repository import SessionRepository

from .command import LogoutCommand


class LogoutHandler:
    def __init__(self, session_repository: SessionRepository) -> None:
        self._sessions = session_repository

    def __call__(self, command: LogoutCommand) -> None:
        try:
            session_id = SessionId.create(uuid.UUID(command.session_id))
        except (ValueError, AttributeError) as exc:  # invalid UUID
            raise ValueError("Invalid session identifier") from exc
        session = self._sessions.get_by_id(session_id)
        if not session:
            return
        session.revoke()
        self._sessions.update(session)

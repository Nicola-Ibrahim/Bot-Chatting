"""Handler responsible for issuing short-lived access tokens."""

from __future__ import annotations

from datetime import timedelta
from typing import Any, Callable, Mapping

from .command import IssueTokenCommand
from .dto import IssuedTokenDTO

TokenFactory = Callable[[Mapping[str, Any], timedelta | None], str]


class IssueTokenHandler:
    def __init__(self, token_factory: TokenFactory) -> None:
        self._token_factory = token_factory

    def __call__(self, command: IssueTokenCommand) -> IssuedTokenDTO:
        claims: dict[str, Any] = {"sub": command.account_id}
        if command.session_id:
            claims["sid"] = command.session_id
        if command.extra_claims:
            claims.update(command.extra_claims)
        expires_delta = None
        if command.expires_in_seconds:
            expires_delta = timedelta(seconds=command.expires_in_seconds)
        token = self._token_factory(claims, expires_delta)
        return IssuedTokenDTO(access_token=token)

"""Session aggregate representing an authenticated session for an account."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from src.building_blocks.domain.aggregate_root import AggregateRoot

from ..account.value_objects.account_id import AccountId
from .events.session_expired_event import SessionExpiredEvent
from .events.session_issued_event import SessionIssuedEvent
from .events.session_revoked_event import SessionRevokedEvent
from .rules.session_expiration_must_be_future_rule import SessionExpirationMustBeFutureRule
from .value_objects.refresh_token import RefreshToken
from .value_objects.session_id import SessionId
from .value_objects.session_status import SessionStatus


@dataclass(eq=False)
class Session(AggregateRoot[SessionId]):
    _id: SessionId
    _account_id: AccountId
    _refresh_token: RefreshToken
    _expires_at: datetime
    _status: SessionStatus = field(default_factory=SessionStatus.active)

    @property
    def account_id(self) -> AccountId:
        return self._account_id

    @property
    def refresh_token(self) -> RefreshToken:
        return self._refresh_token

    @property
    def expires_at(self) -> datetime:
        return self._expires_at

    @property
    def is_active(self) -> bool:
        return self._status.is_active

    @classmethod
    def issue(cls, account_id: AccountId, refresh_token: RefreshToken, expires_at: datetime) -> "Session":
        cls.check_rules(SessionExpirationMustBeFutureRule(expires_at=expires_at))
        session = cls(
            _id=SessionId.create(),
            _account_id=account_id,
            _refresh_token=refresh_token,
            _expires_at=expires_at,
        )
        session.record_event(SessionIssuedEvent(session_id=str(session.id.value), account_id=str(account_id.value)))
        return session

    def revoke(self) -> None:
        if self._status.is_active:
            self._status = self._status.revoke()
            self.record_event(
                SessionRevokedEvent(session_id=str(self.id.value), account_id=str(self.account_id.value))
            )

    def expire(self) -> None:
        if self._status.is_active:
            self._status = self._status.revoke()
            self.record_event(
                SessionExpiredEvent(session_id=str(self.id.value), account_id=str(self.account_id.value))
            )

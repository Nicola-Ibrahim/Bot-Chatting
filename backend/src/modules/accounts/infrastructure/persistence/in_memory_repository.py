"""In-memory repository implementations for development and testing."""

from __future__ import annotations

from typing import Dict, Iterable, Optional

from src.modules.accounts.domain.aggregates.account.account import Account
from src.modules.accounts.domain.aggregates.account.value_objects.account_id import AccountId
from src.modules.accounts.domain.aggregates.role.value_objects.role_id import RoleId
from src.modules.accounts.domain.aggregates.session.session import Session
from src.modules.accounts.domain.aggregates.session.value_objects.session_id import SessionId
from src.modules.accounts.domain.interfaces import AccountRepository, SessionRepository


class InMemoryAccountRepository(AccountRepository):
    def __init__(self) -> None:
        self._by_id: Dict[str, Account] = {}
        self._by_email: Dict[str, str] = {}

    def add(self, account: Account) -> None:
        key = str(account.id.value)
        self._by_id[key] = account
        self._by_email[str(account.email)] = key

    def update(self, account: Account) -> None:
        key = str(account.id.value)
        self._by_id[key] = account
        self._by_email[str(account.email)] = key

    def get_by_id(self, account_id: AccountId) -> Optional[Account]:
        return self._by_id.get(str(account_id.value))

    def get_by_email(self, email: str) -> Optional[Account]:
        account_id = self._by_email.get(email)
        return self._by_id.get(account_id) if account_id else None

    def exists_by_email(self, email: str) -> bool:
        return email in self._by_email

    def list_accounts(self) -> Iterable[Account]:
        return list(self._by_id.values())

    def remove(self, account_id: AccountId) -> None:
        key = str(account_id.value)
        account = self._by_id.pop(key, None)
        if account:
            self._by_email.pop(str(account.email), None)

    def assign_role(self, account_id: AccountId, role_id: RoleId) -> None:
        account = self.get_by_id(account_id)
        if not account:
            raise ValueError("Account not found")
        account.assign_role(role_id)


class InMemorySessionRepository(SessionRepository):
    def __init__(self) -> None:
        self._sessions: Dict[str, Session] = {}
        self._by_account: Dict[str, set[str]] = {}

    def add(self, session: Session) -> None:
        key = str(session.id.value)
        self._sessions[key] = session
        self._by_account.setdefault(str(session.account_id.value), set()).add(key)

    def update(self, session: Session) -> None:
        self._sessions[str(session.id.value)] = session

    def get_by_id(self, session_id: SessionId) -> Optional[Session]:
        return self._sessions.get(str(session_id.value))

    def list_for_account(self, account_id: AccountId) -> Iterable[Session]:
        keys = self._by_account.get(str(account_id.value), set())
        return [self._sessions[key] for key in keys]

    def revoke_all_for_account(self, account_id: AccountId) -> None:
        for session in self.list_for_account(account_id):
            session.revoke()
            self.update(session)

"""Aggregate root representing an account within the system."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from src.building_blocks.domain.aggregate_root import AggregateRoot

from ..role.value_objects.role_id import RoleId
from .events.account_deactivated_event import AccountDeactivatedEvent
from .events.account_registered_event import AccountRegisteredEvent
from .events.account_verified_event import AccountVerifiedEvent
from .events.password_changed_event import PasswordChangedEvent
from .value_objects.account_id import AccountId
from .value_objects.account_status import AccountStatus
from .value_objects.email import Email
from .value_objects.hashed_password import HashedPassword


@dataclass(eq=False)
class Account(AggregateRoot[AccountId]):
    _id: AccountId
    _email: Email
    _password: HashedPassword
    _status: AccountStatus = field(default_factory=AccountStatus.create)
    _role_ids: set[RoleId] = field(default_factory=set, repr=False)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------
    @property
    def email(self) -> Email:
        return self._email

    @property
    def hashed_password(self) -> HashedPassword:
        return self._password

    @property
    def is_verified(self) -> bool:
        return self._status.is_verified

    @property
    def is_active(self) -> bool:
        return self._status.is_active

    @property
    def role_ids(self) -> Iterable[RoleId]:
        return tuple(self._role_ids)

    # ------------------------------------------------------------------
    # Behaviour
    # ------------------------------------------------------------------
    @classmethod
    def register(cls, email: Email, hashed_password: HashedPassword) -> "Account":
        account = cls(_id=AccountId.create(), _email=email, _password=hashed_password)
        account.record_event(AccountRegisteredEvent(account_id=str(account.id.value), email=str(email)))
        return account

    def verify(self) -> None:
        if not self._status.is_verified:
            self._status = self._status.mark_verified()
            self.record_event(AccountVerifiedEvent(account_id=str(self.id.value)))

    def deactivate(self) -> None:
        if self._status.is_active:
            self._status = self._status.deactivate()
            self.record_event(AccountDeactivatedEvent(account_id=str(self.id.value)))

    def activate(self) -> None:
        if not self._status.is_active:
            self._status = self._status.activate()

    def change_email(self, new_email: Email) -> None:
        if str(self._email) != str(new_email):
            self._email = new_email
            self.touch()

    def change_password(self, new_hashed_password: HashedPassword) -> None:
        if self._password != new_hashed_password:
            self._password = new_hashed_password
            self.record_event(PasswordChangedEvent(account_id=str(self.id.value)))

    def assign_role(self, role_id: RoleId) -> None:
        if role_id not in self._role_ids:
            self._role_ids.add(role_id)
            self.touch()

    def remove_role(self, role_id: RoleId) -> None:
        if role_id in self._role_ids:
            self._role_ids.remove(role_id)
            self.touch()

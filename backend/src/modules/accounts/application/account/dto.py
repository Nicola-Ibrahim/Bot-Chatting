"""DTOs shared across account command/query handlers."""

from dataclasses import dataclass

from src.modules.accounts.domain.account.account import Account


@dataclass(slots=True, frozen=True)
class AccountDTO:
    id: str
    email: str
    is_verified: bool
    is_active: bool
    roles: tuple[str, ...]


def to_account_dto(account: Account) -> AccountDTO:
    """Map an account aggregate to a transport-friendly DTO."""
    role_ids = tuple(str(role_id.value) for role_id in account.role_ids)
    return AccountDTO(
        id=str(account.id.value),
        email=str(account.email),
        is_verified=account.is_verified,
        is_active=account.is_active,
        roles=role_ids,
    )

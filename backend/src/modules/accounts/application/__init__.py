"""Application layer for the accounts module."""

from .access_control.assign_role.handler import AssignRoleHandler  # noqa: F401
from .account import (  # noqa: F401
    GetAccountHandler,
    ListAccountsHandler,
    RemoveAccountHandler,
    UpdateAccountHandler,
    VerifyAccountHandler,
)
from .authentication.login.handler import LoginHandler  # noqa: F401
from .authentication.logout.handler import LogoutHandler  # noqa: F401
from .registration.register_account.handler import RegisterAccountHandler  # noqa: F401

__all__ = [
    "AssignRoleHandler",
    "GetAccountHandler",
    "ListAccountsHandler",
    "RemoveAccountHandler",
    "UpdateAccountHandler",
    "VerifyAccountHandler",
    "LoginHandler",
    "LogoutHandler",
    "RegisterAccountHandler",
]

"""Application layer for the accounts module.

This package exposes the high‑level services used by the API layer to
interact with the accounts bounded context.
"""

from .services.accounts_service import AccountsService  # noqa: F401

__all__ = ["AccountsService"]

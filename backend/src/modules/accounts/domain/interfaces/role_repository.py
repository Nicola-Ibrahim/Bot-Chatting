"""Repository interface for roles."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Optional

from ..aggregates.role.role import Role
from ..aggregates.role.value_objects.role_id import RoleId


class RoleRepository(ABC):
    @abstractmethod
    def add(self, role: Role) -> None:
        """Persist a new role aggregate."""

    @abstractmethod
    def get_by_id(self, role_id: RoleId) -> Optional[Role]:
        """Retrieve a role by identifier."""

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Role]:
        """Retrieve a role by name."""

    @abstractmethod
    def list_roles(self) -> Iterable[Role]:
        """Return all defined roles."""

from contextlib import contextmanager
from typing import Dict, Type

from src.building_blocks.infrastructure.unit_of_work import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self._repositories: Dict[Type, object] = {}
        self._committed = False

    def register_repository(self, repo_type: Type, repo_instance: object):
        self._repositories[repo_type] = repo_instance

    def get_repository(self, repo_type: Type):
        return self._repositories.get(repo_type)

    def commit(self):
        """Commit all changes made to the repositories."""
        for repo in self._repositories.values():
            if hasattr(repo, "commit"):
                repo.commit()
        self._committed = True

    def rollback(self):
        """Rollback changes made to the repositories (if supported)."""
        for repo in self._repositories.values():
            if hasattr(repo, "rollback"):
                repo.rollback()

    @contextmanager
    def transaction(self):
        """Provide a transactional scope."""
        try:
            yield self
            self.commit()
        except Exception as e:
            self.rollback()
            raise e

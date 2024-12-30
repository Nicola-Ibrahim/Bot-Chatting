from typing import Type


class AbstractUnitOfWork:
    def register_repository(self, repo_type: Type, repo_instance: object):
        raise NotImplementedError

    def get_repository(self, repo_type: Type):
        raise NotImplementedError

    def commit(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError

    def transaction(self):
        raise NotImplementedError

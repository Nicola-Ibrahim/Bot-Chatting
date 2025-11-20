from src.database.session import SQLAlchemySessionFactory

from .containers import AccountsDIContainer


class AccountsStartUp:
    def __init__(self) -> None:
        self._container: AccountsDIContainer | None = None
        self._session_factory = None

    @property
    def container(self) -> AccountsDIContainer:
        if self._container is None:
            raise RuntimeError("Accounts container not initialized")
        return self._container

    def initialize(
        self,
        *,
        database_url: str,
        enable_registration: bool,
        default_role: str,
    ) -> "AccountsStartUp":
        if not database_url:
            raise ValueError("Accounts configuration requires a 'database_url'")

        config = {
            "enable_registration": enable_registration,
            "default_role": default_role,
        }

        try:
            self._session_factory = SQLAlchemySessionFactory.acquire(database_url)
            self._container = AccountsDIContainer(config=config, session_factory=self._session_factory)
            self._container.init_resources()
            self._container.wire(
                packages=[
                    "src.contexts.accounts.application",
                    "src.contexts.accounts.module",
                ]
            )
            return self
        except Exception as ex:
            raise RuntimeError("Accounts module bootstrap failed") from ex

    def stop(self) -> None:
        try:
            if self._container:
                self._container.shutdown_resources()
                self._container.unwire()
        finally:
            SQLAlchemySessionFactory.release(self._database_url)
            self._container = None

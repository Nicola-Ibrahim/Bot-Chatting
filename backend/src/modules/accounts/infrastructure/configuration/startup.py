from .containers import AccountsDIContainer


class AccountsStartUp:
    def __init__(self) -> None:
        self._container: AccountsDIContainer | None = None

    @property
    def container(self) -> AccountsDIContainer:
        if self._container is None:
            raise RuntimeError("Accounts container not initialized")
        return self._container

    def initialize(self, config: dict) -> None:
        try:
            self._container = AccountsDIContainer()
            # expected: {"database": {"url": "..."}}
            self._container.config.from_dict(config)
            self._container.init_resources()
            self._container.wire(
                packages=[
                    "src.contexts.accounts.application",
                    "src.contexts.accounts.module",
                ]
            )
        except Exception as ex:
            raise RuntimeError("Accounts module bootstrap failed") from ex

    def stop(self) -> None:
        try:
            if self._container:
                self._container.shutdown_resources()
                self._container.unwire()
        finally:
            self._container = None

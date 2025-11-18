from .containers import DatabaseDIContainer


class DatabaseStartUp:
    def __init__(self) -> None:
        self._container: DatabaseDIContainer | None = None

    @property
    def container(self) -> DatabaseDIContainer:
        if self._container is None:
            raise RuntimeError("Database container not initialized")
        return self._container

    def initialize(self, config: dict) -> None:
        try:
            self._container = DatabaseDIContainer()
            self._container.config.from_dict(config)  # {"url": "..."}
            self._container.init_resources()
            # No wire() needed unless you use Provide[...] from this package
        except Exception as ex:
            raise RuntimeError("Database bootstrap failed") from ex

    def stop(self) -> None:
        try:
            if self._container:
                self._container.shutdown_resources()
        finally:
            self._container = None

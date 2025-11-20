from typing import Any

from src.database.configuration.startup import DatabaseStartUp

from .modules.accounts.infrastructure.configuration.startup import AccountsStartUp
from .modules.chats.infrastructure.configuration.startup import ChatsStartUp


class _BackendHandles:
    """Handles the lifecycle of module startups."""

    def __init__(self, startups: dict[str, object]) -> None:
        self._startups = startups

    def shutdown(self) -> None:
        for s in self._startups.values():
            try:
                s.stop()
            except Exception:
                pass


class BackendInitializer:
    """Initializes all modules based on provided settings."""

    _modules = {
        "database": DatabaseStartUp(),
        "chats": ChatsStartUp(),
        "accounts": AccountsStartUp(),
    }

    @classmethod
    def initialize(cls, config: dict[str, dict[str, Any]]) -> _BackendHandles:
        startups = {}
        for module_name, startup_cls in cls._modules.items():
            # Raise error if unknown module
            if module_name not in cls._modules:
                raise ValueError(f"Unknown module '{module_name}' in settings")

            # Initialize module startup with its settings
            module_settings = config.get(module_name, {})
            print(f"Initializing module '{module_name}' with settings: {module_settings}")
            startup_instance = startup_cls.initialize(config=module_settings)
            startups[module_name] = startup_instance

        return _BackendHandles(startups)

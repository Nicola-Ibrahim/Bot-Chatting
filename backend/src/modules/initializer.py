from typing import Any

from src.database.configuration.startup import DatabaseStartUp

from .accounts.infrastructure.configuration.startup import AccountsStartUp
from .chats.infrastructure.configuration.startup import ChatsStartUp
from .llm_backend.infrastructure.configuration.startup import LLMsStartUp


class _ModuleHandles:
    """Handles the lifecycle of module startups."""

    def __init__(self, startups: dict[str, object]) -> None:
        self._startups = startups

    def shutdown(self) -> None:
        for s in self._startups.values():
            try:
                s.stop()
            except Exception:
                pass


class ModuleInitializer:
    """Initializes all modules based on provided settings."""

    _modules = {
        "database": DatabaseStartUp,
        "chats": ChatsStartUp,
        "accounts": AccountsStartUp,
        "llm": LLMsStartUp,
    }

    @staticmethod
    def _as_dict(settings: Any) -> dict[str, Any]:
        if isinstance(settings, dict):
            return settings
        raise TypeError("settings must be a dict")

    @classmethod
    def initialize(cls, settings: dict) -> _ModuleHandles:
        cfg = cls._as_dict(settings)

        startups = {}
        for module_name, startup_cls in cls._modules.items():
            # Raise error if unknown module
            if module_name not in cls._modules:
                raise ValueError(f"Unknown module '{module_name}' in settings")

            # Initialize module startup with its settings
            module_settings = cfg.get(module_name, {})
            startup_instance = startup_cls(module_settings)
            startup_instance.start()
            startups[module_name] = startup_instance

        return _ModuleHandles(startups)

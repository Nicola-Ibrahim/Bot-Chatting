from typing import Dict, Type

from .chats.infrastructure.configuration.startup import ChatsStartUp
from .llm_backend.infrastructure.configuration.startup import LLMsStartUp
from .users.infrastructure.configuration.startup import UsersStartUp


class ModuleInitializer:
    """Centralized module initialization manager"""

    _modules = {"chats": ChatsStartUp, "llm": LLMsStartUp, "users": UsersStartUp}

    @classmethod
    def initialize(cls, modules: list[str] = None) -> None:
        """
        Initialize specified modules or all modules if none specified

        Args:
            modules: List of module names to initialize (e.g., ['chats', 'llm'])
        """
        to_initialize = cls._modules.keys() if modules is None else modules

        for module_name in to_initialize:
            if module_name in cls._modules:
                print(f"Initializing {module_name} module...")
                cls._modules[module_name].initialize()
            else:
                raise ValueError(f"Unknown module: {module_name}")

    @classmethod
    def get_available_modules(cls) -> Dict[str, Type]:
        """Return available modules for initialization"""
        return cls._modules.copy()

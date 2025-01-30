import os

env = os.getenv("ENV", "dev")

if env == "prod":
    from .prod import prod_settings as settings
else:
    from .dev import dev_settings as settings

__all__ = ["settings"]

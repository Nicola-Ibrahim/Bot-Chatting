import asyncio
from contextlib import asynccontextmanager

import uvicorn

from src.api.main import app as FastAPIApp

from .api.core.config import get_settings
from .initializer import BackendInitializer


@asynccontextmanager
async def backend_runtime():
    """Async context that starts and stops the backend modules."""

    handles = BackendInitializer.initialize(
        config={
            "database": {"url": "postgresql+asyncpg://dev_user:dev_password@localhost:5432/chatbot_dev"},
            "accounts": {"enable_registration": True, "default_role": "user"},
            "chats": {"max_active_chats_per_user": 5},
        }
    )
    try:
        yield handles
    finally:
        handles.shutdown()


async def server():
    """Main entry point: Initializes DI and runs the app."""

    settings = get_settings()

    async with backend_runtime():
        config = uvicorn.Config(
            app=FastAPIApp,
            host=getattr(settings, "HOST", "0.0.0.0"),
            port=getattr(settings, "PORT", 8000),
            reload=bool(getattr(settings, "DEBUG", False)),
            log_level="debug" if getattr(settings, "DEBUG", False) else "info",
        )
        server = uvicorn.Server(config)
        await server.serve()


if __name__ == "__main__":
    asyncio.run(server())

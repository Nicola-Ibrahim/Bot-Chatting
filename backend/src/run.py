from contextlib import asynccontextmanager

from src.api.main import app as FastAPIApp

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

    async with backend_runtime() as handles:
        FastAPIApp.run()


if __name__ == "__main__":
    server()

from src.api.main import app as FastAPIApp

from .initializer import BackendInitializer


def main():
    """Main entry point: Initializes DI and runs the app."""
    BackendInitializer.initialize(
        config={
            "database": {"url": "postgresql+asyncpg://dev_user:dev_password@localhost:5432/chatbot_dev"},
            "accounts": {"enable_registration": True, "default_role": "user"},
            "chats": {"max_active_chats_per_user": 5},
        }
    )
    FastAPIApp.run()


if __name__ == "__main__":
    main()

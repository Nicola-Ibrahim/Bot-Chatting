from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# If you already have a DatabaseConnectionManager, you can keep using it.
# Here's a direct SQLAlchemy version for clarity.
class DatabaseDIContainer(containers.DeclarativeContainer):
    config = providers.Configuration()  # expects: {"url": "postgresql+psycopg://..."}

    engine = providers.Singleton(
        create_engine,
        config.url,
        pool_pre_ping=True,
        future=True,
    )

    session_factory = providers.Singleton(
        sessionmaker,
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )

    # Per-use / per-request session factory -> returns a new Session each call
    session = providers.Factory(lambda sf: sf(), sf=session_factory)

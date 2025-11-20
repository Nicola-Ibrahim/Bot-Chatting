from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseDIContainer(containers.DeclarativeContainer):
    """Infrastructure-level DB container: one engine, one session_factory."""

    config = providers.Configuration()  # expects: {"url": "postgresql+asyncpg://..."}

    # One Engine (connection pool) for the whole process
    engine = providers.Singleton(
        create_engine,
        url=config.url,
        pool_pre_ping=True,
        future=True,
    )

    # Singleton session factory bound to the engine
    session_factory = providers.Singleton(
        sessionmaker,
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )

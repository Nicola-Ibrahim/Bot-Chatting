from threading import Lock
from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


class SQLAlchemySessionFactory:
    """Utility that returns singleton engines and session factories per DB URL."""

    _engines: Dict[str, Engine] = {}
    _session_factories: Dict[str, sessionmaker] = {}
    _ref_counts: Dict[str, int] = {}
    _lock = Lock()

    @classmethod
    def acquire(cls, url: str) -> sessionmaker:
        if not url:
            raise ValueError("Database URL must be provided")

        with cls._lock:
            factory = cls._session_factories.get(url)
            if factory is None:
                engine = cls._engines.get(url)
                if engine is None:
                    engine = create_engine(url, pool_pre_ping=True, future=True)
                    cls._engines[url] = engine

                factory = sessionmaker(
                    bind=engine,
                    autoflush=False,
                    expire_on_commit=False,
                )
                cls._session_factories[url] = factory

            cls._ref_counts[url] = cls._ref_counts.get(url, 0) + 1
            return factory

    @classmethod
    def release(cls, url: str | None) -> None:
        if not url:
            return

        with cls._lock:
            ref_count = cls._ref_counts.get(url, 0)
            if ref_count <= 1:
                cls._ref_counts.pop(url, None)
                cls._session_factories.pop(url, None)
                engine = cls._engines.pop(url, None)
                if engine:
                    engine.dispose()
            else:
                cls._ref_counts[url] = ref_count - 1

    @classmethod
    def dispose_all(cls) -> None:
        with cls._lock:
            for url in list(cls._engines.keys()):
                engine = cls._engines.pop(url)
                engine.dispose()
            cls._session_factories.clear()
            cls._ref_counts.clear()

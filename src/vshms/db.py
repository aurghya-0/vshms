"""Database engine, session factory and the declarative base for all models.

The engine and session factory belong to the app (``app.state``), not to module
globals, so every test can run against its own throwaway database.

Sync-related session events (outbox capture, HLC stamping, rejecting bulk
updates on syncable tables) are added here by task A3 in docs/TASKS.md.
SQLCipher encryption is added by task C2.
"""

from collections.abc import Iterator
from typing import Any

from fastapi import Request
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from vshms.config import Settings


class Base(DeclarativeBase):
    """Declarative base for every VSHMS model."""


def _set_sqlite_pragmas(dbapi_connection: Any, _record: Any) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=FULL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA busy_timeout=5000")
    cursor.close()


def make_engine(settings: Settings) -> Engine:
    url = settings.resolved_database_url
    if url.startswith("sqlite"):
        settings.data_dir.mkdir(parents=True, exist_ok=True)
        engine = create_engine(url, connect_args={"check_same_thread": False})
        event.listen(engine, "connect", _set_sqlite_pragmas)
        return engine
    return create_engine(url, pool_pre_ping=True)


def make_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, expire_on_commit=False)


def get_session(request: Request) -> Iterator[Session]:
    """FastAPI dependency: one session per request. Services commit explicitly."""
    factory: sessionmaker[Session] = request.app.state.session_factory
    with factory() as session:
        yield session

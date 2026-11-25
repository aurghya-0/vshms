"""Shared fixtures. Every test gets its own data directory and SQLite database."""

from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from vshms.config import Settings
from vshms.db import make_engine, make_session_factory
from vshms.main import create_app


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    """Settings pointing at a throwaway data directory. Never touches ~/.vshms."""
    return Settings(data_dir=tmp_path / "data", debug=True)


@pytest.fixture
def engine(settings: Settings) -> Iterator[Engine]:
    engine = make_engine(settings)
    yield engine
    engine.dispose()


@pytest.fixture
def session(engine: Engine) -> Iterator[Session]:
    """A session on a real (temporary) SQLite database, for unit tests of services."""
    with make_session_factory(engine)() as session:
        yield session


@pytest.fixture
def app(settings: Settings) -> Iterator[FastAPI]:
    app = create_app(settings)
    yield app
    app.state.engine.dispose()


@pytest.fixture
def client(app: FastAPI) -> Iterator[TestClient]:
    with TestClient(app) as client:
        yield client

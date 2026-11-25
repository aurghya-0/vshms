"""The request-scoped session reaches a real SQLite database with the expected settings."""

from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session

from vshms.db import get_session


def test_request_session_uses_wal_sqlite_with_foreign_keys(app: FastAPI) -> None:
    @app.get("/_test/pragmas")
    def pragmas(session: Annotated[Session, Depends(get_session)]) -> dict[str, object]:
        return {
            "journal_mode": session.execute(text("PRAGMA journal_mode")).scalar_one(),
            "foreign_keys": session.execute(text("PRAGMA foreign_keys")).scalar_one(),
        }

    with TestClient(app) as client:
        response = client.get("/_test/pragmas")

    assert response.json() == {"journal_mode": "wal", "foreign_keys": 1}


def test_committed_data_survives_a_new_session(app: FastAPI) -> None:
    factory = app.state.session_factory
    with factory() as session:
        session.execute(text("CREATE TABLE note (id INTEGER PRIMARY KEY, body TEXT)"))
        session.execute(text("INSERT INTO note (body) VALUES ('saved')"))
        session.commit()

    with factory() as session:
        assert session.execute(text("SELECT body FROM note")).scalar_one() == "saved"


def test_uncommitted_data_is_rolled_back(app: FastAPI) -> None:
    factory = app.state.session_factory
    with factory() as session:
        session.execute(text("CREATE TABLE note (id INTEGER PRIMARY KEY, body TEXT)"))
        session.commit()

    with factory() as session:
        session.execute(text("INSERT INTO note (body) VALUES ('draft')"))
        # Leaving the block without commit() rolls back, as after a crash mid-request.

    with factory() as session:
        assert session.execute(text("SELECT COUNT(*) FROM note")).scalar_one() == 0

from pathlib import Path

import pytest

from vshms.config import Mode, Settings


def test_default_database_is_sqlite_file_in_data_dir(tmp_path: Path) -> None:
    settings = Settings(data_dir=tmp_path)

    assert settings.resolved_database_url == f"sqlite:///{tmp_path / 'vshms.db'}"


def test_explicit_database_url_wins(tmp_path: Path) -> None:
    url = "postgresql://relay@localhost/vshms"
    settings = Settings(data_dir=tmp_path, database_url=url)

    assert settings.resolved_database_url == url


def test_mode_is_read_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("VSHMS_MODE", "hub")

    assert Settings().mode is Mode.HUB

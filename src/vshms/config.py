"""Application settings, read from environment variables prefixed with ``VSHMS_``."""

from enum import StrEnum
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Mode(StrEnum):
    """How this install runs (see PLAN.md §5.1)."""

    SOLO = "solo"  # single device, no network
    HUB = "hub"  # serves other devices on the LAN
    RELAY = "relay"  # cloud relay on PostgreSQL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="VSHMS_", env_file=".env", extra="ignore")

    mode: Mode = Mode.SOLO
    debug: bool = False
    data_dir: Path = Path.home() / ".vshms"
    # Leave empty to use an SQLite file inside data_dir.
    database_url: str = ""
    host: str = "127.0.0.1"
    port: int = 8710

    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return f"sqlite:///{self.data_dir / 'vshms.db'}"


@lru_cache
def get_settings() -> Settings:
    return Settings()

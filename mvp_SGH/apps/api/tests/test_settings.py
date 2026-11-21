import pytest
from pydantic import ValidationError

from app.config.settings import Settings


def test_database_url_is_required(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(ValidationError, match="DATABASE_URL"):
        Settings()


def test_database_url_cannot_be_blank(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", " ")

    with pytest.raises(ValidationError, match="DATABASE_URL"):
        Settings()


def test_database_url_is_loaded_from_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database_url = "postgresql+asyncpg://test:test@localhost:5432/test"
    monkeypatch.setenv("DATABASE_URL", database_url)

    assert Settings().DATABASE_URL == database_url


def test_database_read_url_is_optional(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DATABASE_READ_URL", raising=False)

    assert Settings().DATABASE_READ_URL is None

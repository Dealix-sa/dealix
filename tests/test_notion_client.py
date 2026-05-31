"""NotionClient configuration, mock short-circuit, and upsert create/update paths."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from core.config.settings import get_settings


@pytest.fixture(autouse=True)
def _clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_configured_false_without_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NOTION_API_KEY", raising=False)
    from integrations.notion import NotionClient

    client = NotionClient()
    assert client.configured is False
    # Not configured implies mock (zero-HTTP) behavior.
    assert client.mock is True


def test_mock_true_when_mock_mode_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NOTION_API_KEY", "secret_abc")
    monkeypatch.setenv("NOTION_MOCK_MODE", "true")
    from integrations.notion import NotionClient

    client = NotionClient()
    assert client.configured is True
    assert client.mock is True


async def test_upsert_under_mock_makes_zero_http(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NOTION_API_KEY", "secret_abc")
    monkeypatch.setenv("NOTION_MOCK_MODE", "true")
    from integrations.notion import NotionClient, title_prop

    client = NotionClient()
    spy = AsyncMock()
    monkeypatch.setattr(client, "_request", spy)

    result = await client.upsert_row(
        "db1", external_id="x-1", properties={"Name": title_prop("hi")}
    )

    assert result.success is True
    assert result.mock is True
    spy.assert_not_called()


async def test_upsert_creates_when_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NOTION_API_KEY", "secret_abc")
    monkeypatch.setenv("NOTION_MOCK_MODE", "false")
    from integrations.notion import NotionClient, title_prop

    client = NotionClient()
    calls: list[tuple[str, str]] = []

    async def fake_request(method: str, path: str, json=None):
        calls.append((method, path))
        if path.endswith("/query"):
            return {"results": []}  # not found -> create
        return {"id": "new_page_123"}

    monkeypatch.setattr(client, "_request", fake_request)

    result = await client.upsert_row(
        "db1", external_id="x-1", properties={"Name": title_prop("hi")}
    )

    assert result.success is True
    assert result.created is True
    assert result.page_id == "new_page_123"
    methods = [m for m, _ in calls]
    assert methods == ["POST", "POST"]  # query then create
    assert calls[-1][1] == "/pages"


async def test_upsert_updates_when_found(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NOTION_API_KEY", "secret_abc")
    monkeypatch.setenv("NOTION_MOCK_MODE", "false")
    from integrations.notion import NotionClient, title_prop

    client = NotionClient()
    calls: list[tuple[str, str]] = []

    async def fake_request(method: str, path: str, json=None):
        calls.append((method, path))
        if path.endswith("/query"):
            return {"results": [{"id": "existing_page_9"}]}  # found -> patch
        return {"id": "existing_page_9"}

    monkeypatch.setattr(client, "_request", fake_request)

    result = await client.upsert_row(
        "db1", external_id="x-1", properties={"Name": title_prop("hi")}
    )

    assert result.success is True
    assert result.created is False
    assert result.page_id == "existing_page_9"
    assert calls[0][0] == "POST"  # query
    assert calls[-1] == ("PATCH", "/pages/existing_page_9")


async def test_find_database_returns_none_when_not_configured(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("NOTION_API_KEY", raising=False)
    from integrations.notion import NotionClient

    client = NotionClient()
    spy = AsyncMock()
    monkeypatch.setattr(client, "_request", spy)

    assert await client.find_database("KPIs") is None
    spy.assert_not_called()

"""Extra path coverage for integrations.notion.

Covers the transport (`_request` success + 429 retry), `_headers`,
`find_database`, `query_by_external_id` not-configured, the configured
mock-mode upsert branch, `append_blocks` (mock + real), and every
`markdown_to_blocks` branch. No live network — httpx is faked / `_request`
is mocked.
"""

from __future__ import annotations

import httpx
import pytest

import integrations.notion as notion
from core.config.settings import get_settings
from core.errors import RateLimitError


@pytest.fixture(autouse=True)
def _clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def _client_with_key(monkeypatch, *, mock_mode: bool = False) -> notion.NotionClient:
    monkeypatch.setenv("NOTION_API_KEY", "secret_test_key")
    monkeypatch.setenv("NOTION_MOCK_MODE", "true" if mock_mode else "false")
    get_settings.cache_clear()
    return notion.NotionClient()


# ── markdown_to_blocks (all branches) ───────────────────────────────
def test_markdown_to_blocks_covers_all_branches():
    md = "# H1\n## H2\n### H3\n- bullet\n* star\n\nparagraph"
    blocks = notion.markdown_to_blocks(md)
    assert [b["type"] for b in blocks] == [
        "heading_1",
        "heading_2",
        "heading_3",
        "bulleted_list_item",
        "bulleted_list_item",
        "paragraph",
    ]


# ── _headers ────────────────────────────────────────────────────────
def test_headers_with_key(monkeypatch):
    client = _client_with_key(monkeypatch)
    headers = client._headers()
    assert headers["Authorization"] == "Bearer secret_test_key"
    assert headers["Notion-Version"]
    assert headers["Content-Type"] == "application/json"


def test_headers_without_key_raises(monkeypatch):
    monkeypatch.delenv("NOTION_API_KEY", raising=False)
    get_settings.cache_clear()
    client = notion.NotionClient()
    with pytest.raises(RateLimitError):
        client._headers()


# ── _request transport ──────────────────────────────────────────────
class _FakeResp:
    def __init__(self, status_code, json_data=None, headers=None):
        self.status_code = status_code
        self._json = json_data or {}
        self.headers = headers or {}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(
                "error",
                request=httpx.Request("POST", "http://x"),
                response=httpx.Response(self.status_code),
            )

    def json(self):
        return self._json


class _FakeAsyncClient:
    """Async-context-manager httpx.AsyncClient stand-in serving queued responses."""

    def __init__(self, responses):
        self._responses = list(responses)

    def __call__(self, *args, **kwargs):
        return self

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return False

    async def request(self, method, url, json=None, headers=None):
        return self._responses.pop(0)


async def test_request_success(monkeypatch):
    client = _client_with_key(monkeypatch)
    monkeypatch.setattr(notion.httpx, "AsyncClient", _FakeAsyncClient([_FakeResp(200, {"ok": True})]))
    assert await client._request("POST", "/search", json={}) == {"ok": True}


async def test_request_retries_on_429_then_succeeds(monkeypatch):
    client = _client_with_key(monkeypatch)
    monkeypatch.setattr(
        notion.httpx,
        "AsyncClient",
        _FakeAsyncClient([_FakeResp(429, headers={"Retry-After": "0"}), _FakeResp(200, {"ok": 1})]),
    )
    assert await client._request("POST", "/search", json={}) == {"ok": 1}


# ── find_database (configured path) ─────────────────────────────────
async def test_find_database_match_and_nomatch(monkeypatch, mocker):
    client = _client_with_key(monkeypatch)
    mocker.patch.object(
        client,
        "_request",
        mocker.AsyncMock(return_value={"results": [{"id": "db-1", "title": [{"plain_text": "My DB"}]}]}),
    )
    assert await client.find_database("My DB") == "db-1"
    assert await client.find_database("Other DB") is None


# ── query_by_external_id (not configured) ───────────────────────────
async def test_query_by_external_id_not_configured(monkeypatch):
    monkeypatch.delenv("NOTION_API_KEY", raising=False)
    get_settings.cache_clear()
    client = notion.NotionClient()
    assert await client.query_by_external_id("db", "ext-1") is None


# ── upsert: configured + explicit mock mode (zero HTTP) ─────────────
async def test_upsert_configured_mock_mode(monkeypatch):
    client = _client_with_key(monkeypatch, mock_mode=True)
    assert client.configured is True
    assert client.mock is True
    res = await client.upsert_row("db", external_id="x-1", properties={"Name": notion.title_prop("A")})
    assert res.success and res.mock and res.created


# ── append_blocks (mock + real) ─────────────────────────────────────
async def test_append_blocks_mock(monkeypatch):
    client = _client_with_key(monkeypatch, mock_mode=True)
    res = await client.append_blocks("page-1", notion.markdown_to_blocks("# Hi"))
    assert res.success and res.mock


async def test_append_blocks_real(monkeypatch, mocker):
    client = _client_with_key(monkeypatch)
    mocker.patch.object(client, "_request", mocker.AsyncMock(return_value={"id": "page-1"}))
    res = await client.append_blocks("page-1", notion.markdown_to_blocks("# Hi"))
    assert res.success and not res.mock

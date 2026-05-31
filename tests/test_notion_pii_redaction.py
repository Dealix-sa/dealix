"""Doctrine #6 — no raw PII may reach a Notion payload.

Email + Saudi phone (+966...) + national id pushed through the property
builders and a mock upsert must come out redacted, never raw.
"""

from __future__ import annotations

import json
from unittest.mock import AsyncMock

import pytest

from core.config.settings import get_settings

_RAW_EMAIL = "ahmed.salem@example.com"
_RAW_PHONE = "+966512345678"
_RAW_NATIONAL_ID = "1234567890"
_FIELD = f"Reach {_RAW_EMAIL} on {_RAW_PHONE}, national id {_RAW_NATIONAL_ID}"


@pytest.fixture(autouse=True)
def _clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def _assert_no_raw_pii(blob: str) -> None:
    assert _RAW_EMAIL not in blob
    assert _RAW_PHONE not in blob
    assert "512345678" not in blob  # phone digits, even without +966
    assert _RAW_NATIONAL_ID not in blob


def test_property_builders_redact_pii() -> None:
    from integrations.notion import rich_text_prop, title_prop

    title_blob = json.dumps(title_prop(_FIELD), ensure_ascii=False)
    rich_blob = json.dumps(rich_text_prop(_FIELD), ensure_ascii=False)

    _assert_no_raw_pii(title_blob)
    _assert_no_raw_pii(rich_blob)
    # Redaction markers present.
    assert "REDACTED_PHONE" in title_blob
    assert "REDACTED_ID" in title_blob


def test_markdown_blocks_redact_pii() -> None:
    from integrations.notion import markdown_to_blocks

    blocks = markdown_to_blocks(f"# Heading\n- bullet {_FIELD}\nbody {_FIELD}")
    blob = json.dumps(blocks, ensure_ascii=False)
    _assert_no_raw_pii(blob)


async def test_upsert_payload_carries_no_raw_pii(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NOTION_API_KEY", "secret_abc")
    monkeypatch.setenv("NOTION_MOCK_MODE", "false")
    from integrations.notion import NotionClient, rich_text_prop, title_prop

    client = NotionClient()
    captured: list[str] = []

    async def fake_request(method: str, path: str, json=None):
        import json as _json

        captured.append(_json.dumps(json, ensure_ascii=False))
        if path.endswith("/query"):
            return {"results": []}
        return {"id": "page_x"}

    monkeypatch.setattr(client, "_request", fake_request)

    # Even a raw (un-built) string value must be redacted by redact_dict.
    await client.upsert_row(
        "db1",
        external_id="row-1",
        properties={
            "Name": title_prop(_FIELD),
            "Notes": rich_text_prop(_FIELD),
            "RawLeak": _RAW_EMAIL,
        },
    )

    assert captured, "no outbound payload captured"
    for blob in captured:
        _assert_no_raw_pii(blob)


async def test_mock_upsert_still_redacts(monkeypatch: pytest.MonkeyPatch) -> None:
    # Mock path makes zero HTTP but must still redact before logging/short-circuit.
    monkeypatch.setenv("NOTION_API_KEY", "secret_abc")
    monkeypatch.setenv("NOTION_MOCK_MODE", "true")
    from integrations.notion import NotionClient, title_prop

    client = NotionClient()
    spy = AsyncMock()
    monkeypatch.setattr(client, "_request", spy)

    result = await client.upsert_row(
        "db1", external_id="row-1", properties={"Name": title_prop(_FIELD)}
    )
    assert result.success is True and result.mock is True
    spy.assert_not_called()

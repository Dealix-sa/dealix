"""Tests for GET /api/v1/founder/daily-board — read-only surface over the
latest daily lead board JSON. Board dir is overridable via DEALIX_DAILY_BOARD_DIR.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def _client() -> AsyncClient:
    from api.main import app
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@pytest.mark.asyncio
async def test_empty_state_when_no_board(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_DAILY_BOARD_DIR", str(tmp_path))  # empty dir
    async with _client() as client:
        r = await client.get("/api/v1/founder/daily-board")
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["generated"] is False
    assert body["board"] is None
    assert "hint_ar" in body


@pytest.mark.asyncio
async def test_returns_latest_board(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_DAILY_BOARD_DIR", str(tmp_path))
    # Two boards — the newest filename (date) must win.
    (tmp_path / "2026-06-06.json").write_text(
        json.dumps({"on_date": "2026-06-06", "leads_returned": 1}), encoding="utf-8"
    )
    (tmp_path / "2026-06-07.json").write_text(
        json.dumps({"on_date": "2026-06-07", "leads_returned": 10}), encoding="utf-8"
    )
    async with _client() as client:
        r = await client.get("/api/v1/founder/daily-board")
    assert r.status_code == 200
    body = r.json()
    assert body["generated"] is True
    assert body["board_date"] == "2026-06-07"
    assert body["board"]["leads_returned"] == 10
    assert body["hard_gates"]["no_live_send"] is True

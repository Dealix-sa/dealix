"""Tests for POST /api/v1/public/custom-request — the bespoke ("custom
solution") intake. DRAFT-ONLY: captured to the gitignored lead-inbox, never
auto-sent (NO_LIVE_SEND).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def _client() -> AsyncClient:
    from api.main import app
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@pytest.mark.asyncio
async def test_happy_path_persists_to_lead_inbox(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_LEAD_INBOX_PATH", str(tmp_path / "inbox.jsonl"))
    from auto_client_acquisition import lead_inbox

    async with _client() as client:
        r = await client.post("/api/v1/public/custom-request", json={
            "name": "Bassam",
            "company": "Acme Co",
            "email": "founder@acme.sa",
            "phone": "0500000000",
            "what_to_build": "AI رد على leads بالعربي خلال 45 ثانية فوق CRM الحالي",
            "budget_range": "5000-25000",
            "timeline": "30d",
            "consent": True,
        })
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["lead_id"]

    leads = lead_inbox.list_leads(status="new")
    assert any(
        l.get("source") == "landing.custom_form"
        and l.get("request_kind") == "custom_solution"
        and l.get("company") == "Acme Co"
        for l in leads
    )


@pytest.mark.asyncio
async def test_honeypot_is_silently_dropped(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_LEAD_INBOX_PATH", str(tmp_path / "inbox.jsonl"))
    from auto_client_acquisition import lead_inbox

    async with _client() as client:
        r = await client.post("/api/v1/public/custom-request", json={
            "name": "Bot", "company": "Spam", "email": "x@y.sa",
            "what_to_build": "x", "consent": True,
            "website": "http://spam.example",  # honeypot filled
        })
    assert r.status_code == 200
    assert r.json()["ok"] is True
    assert lead_inbox.list_leads(status="new") == []  # nothing persisted


@pytest.mark.asyncio
async def test_missing_what_to_build_is_422(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_LEAD_INBOX_PATH", str(tmp_path / "inbox.jsonl"))
    async with _client() as client:
        r = await client.post("/api/v1/public/custom-request", json={
            "name": "A", "company": "B", "email": "a@b.sa", "consent": True,
        })
    assert r.status_code == 422
    assert r.json()["detail"] == "what_to_build_required"


@pytest.mark.asyncio
async def test_no_consent_is_422(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_LEAD_INBOX_PATH", str(tmp_path / "inbox.jsonl"))
    async with _client() as client:
        r = await client.post("/api/v1/public/custom-request", json={
            "name": "A", "company": "B", "email": "a@b.sa",
            "what_to_build": "something", "consent": False,
        })
    assert r.status_code == 422
    assert r.json()["detail"] == "consent_required"

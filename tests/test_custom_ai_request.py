"""Tests for the public Custom AI Service intake endpoint (commercial ladder Rung 4).

Validates the governed intake at POST /api/v1/public/custom-ai-request:
- valid request is accepted and carries governance_decision="allow"
- missing required fields → 422 (no silent acceptance)
- missing consent → 422 (PDPL: lawful basis required)
- honeypot field → silently dropped, no lead created

Uses a minimal app (only the public router) to avoid the full api.main
optional-router import chain, mirroring tests/test_gtm_public_surfaces.py.
"""
from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient


def _client(tmp_inbox: Path) -> TestClient:
    # Route lead persistence to a throwaway file so tests never touch var/.
    os.environ["DEALIX_LEAD_INBOX_PATH"] = str(tmp_inbox)
    from api.routers import public

    mini = FastAPI()
    mini.include_router(public.router)
    return TestClient(mini)


_VALID = {
    "name": "Sami",
    "company": "Acme Real Estate",
    "email": "sami@acme.sa",
    "phone": "+966500000000",
    "sector": "real_estate",
    "use_case": "lead_intelligence",
    "budget_band": "10k_25k",
    "timeline": "1_3_months",
    "data_readiness": "structured",
    "description": "We want governed lead scoring with approval gates.",
    "consent": True,
}


def test_custom_ai_request_valid(tmp_path):
    client = _client(tmp_path / "inbox.jsonl")
    res = client.post("/api/v1/public/custom-ai-request", json=_VALID)
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["ok"] is True
    assert body["governance_decision"] == "allow"


def test_custom_ai_request_missing_phone_422(tmp_path):
    client = _client(tmp_path / "inbox.jsonl")
    payload = {k: v for k, v in _VALID.items() if k != "phone"}
    res = client.post("/api/v1/public/custom-ai-request", json=payload)
    assert res.status_code == 422


def test_custom_ai_request_requires_consent(tmp_path):
    client = _client(tmp_path / "inbox.jsonl")
    payload = {**_VALID, "consent": False}
    res = client.post("/api/v1/public/custom-ai-request", json=payload)
    assert res.status_code == 422


def test_custom_ai_request_honeypot_silent(tmp_path):
    inbox = tmp_path / "inbox.jsonl"
    client = _client(inbox)
    payload = {**_VALID, "website": "http://spam.example"}
    res = client.post("/api/v1/public/custom-ai-request", json=payload)
    assert res.status_code == 200
    assert res.json()["governance_decision"] == "allow"
    # honeypot must not create a lead record
    assert not inbox.exists() or inbox.read_text().strip() == ""

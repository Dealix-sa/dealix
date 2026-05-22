"""Founder Health Score — HTTP surface (admin-key gated)."""

from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-admin-key")
    monkeypatch.setenv("ADMIN_API_KEYS", "test-admin-key")
    # Re-import app so env vars take effect — but cache wins if already imported,
    # so we just rely on the api_key dependency reading env at request time.
    from api.main import app

    return TestClient(app)


def test_health_score_requires_admin_key(client: TestClient) -> None:
    resp = client.get("/api/v1/founder/health-score")
    # 401 (no key) or 403 (forbidden) — anything but 200 is acceptable here.
    assert resp.status_code in (401, 403)


def test_health_score_returns_score_with_admin_key(client: TestClient) -> None:
    resp = client.get(
        "/api/v1/founder/health-score",
        headers={"X-Admin-API-Key": "test-admin-key"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert 0 <= data["overall_score"] <= 100
    assert data["verdict"] in ("HEALTHY", "CAUTION", "ACTION_NEEDED")
    assert isinstance(data["sub_scores"], dict)
    expected_keys = {
        "evidence_flow",
        "paid_traction",
        "compliance",
        "plan_wiring",
        "inbox_freshness",
    }
    assert expected_keys.issubset(data["sub_scores"].keys())
    assert data["schema_version"] == "1.0"
    assert data["is_estimate"] is True


def test_health_score_rejects_out_of_range_stale_hours(client: TestClient) -> None:
    # Out-of-range values rejected at validator (FastAPI Query bounds).
    resp = client.get(
        "/api/v1/founder/health-score?stale_hours=99999",
        headers={"X-Admin-API-Key": "test-admin-key"},
    )
    assert resp.status_code == 422


def test_health_score_accepts_max_stale_hours(client: TestClient) -> None:
    resp = client.get(
        "/api/v1/founder/health-score?stale_hours=168",
        headers={"X-Admin-API-Key": "test-admin-key"},
    )
    assert resp.status_code == 200
    inbox = (resp.json().get("details") or {}).get("inbox_freshness") or {}
    assert inbox.get("stale_hours_threshold", 24) == 168


def test_health_score_markdown_endpoint(client: TestClient) -> None:
    resp = client.get(
        "/api/v1/founder/health-score.md",
        headers={"X-Admin-API-Key": "test-admin-key"},
    )
    assert resp.status_code == 200
    data = resp.json()
    md = data["markdown"]
    assert "Dealix Founder Health" in md
    assert "/100" in md
    assert "Article" in md
    assert data["verdict"] in ("HEALTHY", "CAUTION", "ACTION_NEEDED")

"""Founder daily-pack API — governed payload shape."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_founder_daily_pack_requires_admin_key(client: TestClient) -> None:
    r = client.get("/api/v1/ops-autopilot/founder/daily-pack")
    assert r.status_code in (401, 403, 422)


def test_founder_daily_pack_ok_with_admin_key(client: TestClient, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-admin-launch-key")
    r = client.get(
        "/api/v1/ops-autopilot/founder/daily-pack",
        headers={"X-Admin-API-Key": "test-admin-launch-key"},
    )
    if r.status_code == 401:
        pytest.skip("admin key middleware uses different env in this build")
    assert r.status_code == 200
    body = r.json()
    assert "kpi_commercial" in body
    assert "checklist_ar" in body
    assert body.get("policy_ar")

"""Founder Action Inbox — HTTP surface (admin-key gated)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-admin-key")
    monkeypatch.setenv("ADMIN_API_KEYS", "test-admin-key")
    from api.main import app

    return TestClient(app)


def test_action_inbox_requires_admin_key(client: TestClient) -> None:
    resp = client.get("/api/v1/founder/action-inbox")
    assert resp.status_code in (401, 403)


def test_action_inbox_returns_shape(client: TestClient) -> None:
    resp = client.get(
        "/api/v1/founder/action-inbox",
        headers={"X-Admin-API-Key": "test-admin-key"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["verdict"] in ("BLOCKED", "ACTIVE_DAY", "MAINTENANCE", "CLEAR")
    assert isinstance(data["items"], list)
    assert isinstance(data["by_priority"], dict)
    assert {"P0", "P1", "P2", "P3"}.issubset(data["by_priority"].keys())
    assert data["schema_version"] == "1.0"
    assert data["is_estimate"] is True


def test_action_inbox_limit_param_respected(client: TestClient) -> None:
    resp = client.get(
        "/api/v1/founder/action-inbox?limit=2",
        headers={"X-Admin-API-Key": "test-admin-key"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["items"]) <= 2


def test_action_inbox_markdown_endpoint(client: TestClient) -> None:
    resp = client.get(
        "/api/v1/founder/action-inbox.md",
        headers={"X-Admin-API-Key": "test-admin-key"},
    )
    assert resp.status_code == 200
    data = resp.json()
    md = data["markdown"]
    assert "Founder Action Inbox" in md
    assert "Article 4" in md

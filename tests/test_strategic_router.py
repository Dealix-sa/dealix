"""Strategic-layer router — list / latest / synthesis endpoints.

Covers the on-demand HTTP surface over the strategic-automation layer.
The DB-unreachable path must degrade to 503 (or an empty list) — never
a 500. The synthesis endpoint is internal analysis only; it must never
trigger an external send.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app

# Strategic briefs are founder-only — the router requires the admin key.
# In the test env no ADMIN_API_KEYS are configured, so any non-empty
# X-Admin-API-Key value passes the guard.
client = TestClient(app, headers={"X-Admin-API-Key": "ci-admin"})


def test_requires_admin_key() -> None:
    """Without the admin key the strategic surface is rejected, not served."""
    resp = TestClient(app).get("/api/v1/strategic/briefs")
    assert resp.status_code in {401, 403}, resp.text


def test_list_briefs_envelope_and_status() -> None:
    """GET /briefs returns a {data, meta, errors} envelope or 503."""
    resp = client.get("/api/v1/strategic/briefs")
    assert resp.status_code in {200, 503}, resp.text
    if resp.status_code == 200:
        body = resp.json()
        assert isinstance(body["data"], list)
        assert "count" in body["meta"]
        assert body["meta"]["limit"] == 20
        assert body["errors"] == []
        assert body["meta"]["hard_gates"]["no_external_send"] is True
        for row in body["data"]:
            assert row["external_send"] is False


def test_list_briefs_accepts_filter_and_limit() -> None:
    """brief_type + limit query params are accepted (never a 500)."""
    resp = client.get(
        "/api/v1/strategic/briefs",
        params={"brief_type": "strategy_synthesis", "limit": 5},
    )
    assert resp.status_code in {200, 503}, resp.text
    if resp.status_code == 200:
        body = resp.json()
        assert body["meta"]["limit"] == 5
        assert body["meta"]["brief_type"] == "strategy_synthesis"
        for row in body["data"]:
            assert row["artifact_type"] == "strategy_synthesis"


def test_list_briefs_rejects_out_of_range_limit() -> None:
    """limit outside 1..200 is a 422 validation error."""
    resp = client.get("/api/v1/strategic/briefs", params={"limit": 0})
    assert resp.status_code == 422, resp.text
    resp = client.get("/api/v1/strategic/briefs", params={"limit": 999})
    assert resp.status_code == 422, resp.text


def test_latest_brief_envelope_and_status() -> None:
    """GET /briefs/latest returns a single brief or data=None — never 500."""
    resp = client.get("/api/v1/strategic/briefs/latest")
    assert resp.status_code in {200, 503}, resp.text
    if resp.status_code == 200:
        body = resp.json()
        assert "found" in body["meta"]
        assert body["errors"] == []
        if body["data"] is not None:
            assert body["meta"]["found"] is True
            assert body["data"]["external_send"] is False


def test_latest_brief_accepts_filter() -> None:
    """brief_type filter is accepted on the latest endpoint."""
    resp = client.get(
        "/api/v1/strategic/briefs/latest",
        params={"brief_type": "growth_scorecard"},
    )
    assert resp.status_code in {200, 503}, resp.text
    if resp.status_code == 200:
        body = resp.json()
        assert body["meta"]["brief_type"] == "growth_scorecard"


def test_run_synthesis_internal_only() -> None:
    """POST /synthesis/run runs internal analysis with no external send."""
    resp = client.post("/api/v1/strategic/synthesis/run")
    assert resp.status_code in {200, 503}, resp.text
    if resp.status_code == 200:
        body = resp.json()
        assert body["errors"] == []
        assert body["meta"]["hard_gates"]["no_external_send"] is True
        result = body["data"]
        assert result["artifact_type"] == "strategy_synthesis"
        assert result["external_send"] is False
        assert "top_3_recommendations" in result
        assert "decision_forks_for_founder" in result

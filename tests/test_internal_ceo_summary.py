"""Internal CEO summary endpoint — smoke + contract test.

Covers api/routers/internal_ceo.py for the founder operating interface
data contract documented at docs/frontend/FOUNDER_INTERFACE_DATA_CONTRACT.md.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app

CLIENT = TestClient(app)


def test_internal_ceo_summary_route_registered() -> None:
    registered_paths = {route.path for route in app.routes}
    assert "/api/v1/internal/ceo/summary" in registered_paths


def test_internal_ceo_summary_returns_data_contract() -> None:
    response = CLIENT.get("/api/v1/internal/ceo/summary")
    assert response.status_code == 200
    body = response.json()
    expected_keys = {
        "top_action",
        "status",
        "risk_flags",
        "cash_collected_sar",
        "approved_outreach",
        "positive_replies",
        "proposals_due",
        "payment_followups_due",
        "last_updated",
    }
    assert expected_keys.issubset(body.keys())
    assert isinstance(body["top_action"], str) and body["top_action"]
    assert isinstance(body["status"], str) and body["status"]
    for numeric_key in (
        "risk_flags",
        "cash_collected_sar",
        "approved_outreach",
        "positive_replies",
        "proposals_due",
        "payment_followups_due",
    ):
        assert isinstance(body[numeric_key], int)
    assert body["last_updated"].endswith("Z")

"""Founder Console v3 — internal API contract tests."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    audit_log = tmp_path / "approval_decisions.csv"
    os.environ["DEALIX_APPROVAL_AUDIT_LOG"] = str(audit_log)
    # Re-import the router module so the env override is picked up.
    import importlib

    from api.routers.internal import founder_console as fc

    importlib.reload(fc)
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(fc.router)
    return TestClient(app)


def test_ceo_summary_returns_api_source(client: TestClient) -> None:
    res = client.get("/api/v1/internal/ceo/summary")
    assert res.status_code == 200
    body = res.json()
    assert body["source"] == "api"
    assert "top_action" in body
    assert "last_updated" in body


def test_sales_funnel_returns_all_stages(client: TestClient) -> None:
    res = client.get("/api/v1/internal/sales/funnel")
    assert res.status_code == 200
    body = res.json()
    for key in (
        "lead_intelligence",
        "a_leads",
        "pending_approval",
        "approved_outreach",
        "sent",
        "replies",
        "positive_replies",
        "samples",
        "proposals",
        "payment_capture",
    ):
        assert key in body


def test_approvals_list_endpoint(client: TestClient) -> None:
    res = client.get("/api/v1/internal/approvals")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_finance_and_distribution_endpoints(client: TestClient) -> None:
    fin = client.get("/api/v1/internal/finance/summary").json()
    dist = client.get("/api/v1/internal/distribution/summary").json()
    assert "cash_collected_sar" in fin
    assert "channels" in dist


def test_approve_decision_writes_audit(client: TestClient, tmp_path: Path) -> None:
    res = client.post(
        "/api/v1/internal/approvals/apt-001/approve",
        json={
            "reason": "Founder approval, ICP fit confirmed",
            "approval_class": "A2",
            "risk_level": "Medium",
            "type": "outreach",
        },
    )
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["status"] == "Approved"
    assert body["policy_result"] == "ALLOW_AFTER_APPROVAL"
    assert body["external_action_allowed"] is True
    assert body["audit_written"] is True
    audit = Path(os.environ["DEALIX_APPROVAL_AUDIT_LOG"]).read_text()
    assert "apt-001" in audit
    assert "approve" in audit
    assert "ALLOW_AFTER_APPROVAL" in audit


def test_reject_decision_writes_audit_and_blocks_external(client: TestClient) -> None:
    res = client.post(
        "/api/v1/internal/approvals/apt-002/reject",
        json={"reason": "Off-ICP", "approval_class": "A2", "risk_level": "Low"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "Rejected"
    assert body["policy_result"] == "DENY"
    assert body["external_action_allowed"] is False
    audit = Path(os.environ["DEALIX_APPROVAL_AUDIT_LOG"]).read_text()
    assert "apt-002" in audit
    assert "reject" in audit


def test_request_edit_decision(client: TestClient) -> None:
    res = client.post(
        "/api/v1/internal/approvals/apt-003/request-edit",
        json={"reason": "Reword opening line", "approval_class": "A1"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "Needs Edit"
    assert body["policy_result"] == "NEEDS_EDIT"
    assert body["external_action_allowed"] is False


def test_a3_cannot_auto_execute(client: TestClient) -> None:
    res = client.post(
        "/api/v1/internal/approvals/apt-004/approve",
        json={
            "reason": "Refund request",
            "approval_class": "A3",
            "risk_level": "Critical",
            "type": "refund",
        },
    )
    assert res.status_code == 200
    body = res.json()
    # Even on approve, A3 must require manual escalation, not external auto-action.
    assert body["external_action_allowed"] is False
    assert "A3" in body["policy_result"]


def test_approve_rejects_mismatched_decision(client: TestClient) -> None:
    res = client.post(
        "/api/v1/internal/approvals/apt-005/approve",
        json={"decision": "reject", "approval_class": "A2"},
    )
    assert res.status_code == 400

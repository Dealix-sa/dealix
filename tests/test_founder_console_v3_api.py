"""Founder Console v3 — internal API contract tests."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.internal import founder_console as fc


@pytest.fixture()
def audit_log(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Redirect the approval audit log into a per-test tmp_path."""
    path = tmp_path / "approval_decisions.csv"
    monkeypatch.setattr(fc, "_AUDIT_LOG_PATH", path)
    return path


@pytest.fixture()
def client(audit_log: Path) -> TestClient:
    app = FastAPI()
    app.include_router(fc.router)
    return TestClient(app)


# ── Read endpoints ────────────────────────────────────────────────
def test_ceo_summary_returns_api_source(client: TestClient) -> None:
    res = client.get("/api/v1/internal/ceo/summary")
    assert res.status_code == 200
    body = res.json()
    assert body["source"] == "api"
    for key in (
        "top_action",
        "status",
        "risk_flags",
        "cash_collected_sar",
        "approved_outreach",
        "positive_replies",
        "proposals_due",
        "payment_followups_due",
        "last_updated",
    ):
        assert key in body


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
        "source",
    ):
        assert key in body


def test_approvals_list_endpoint(client: TestClient) -> None:
    res = client.get("/api/v1/internal/approvals")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_workers_health_endpoint(client: TestClient) -> None:
    res = client.get("/api/v1/internal/workers/health")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_trust_flags_endpoint(client: TestClient) -> None:
    res = client.get("/api/v1/internal/trust/flags")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_finance_summary_endpoint(client: TestClient) -> None:
    res = client.get("/api/v1/internal/finance/summary")
    assert res.status_code == 200
    body = res.json()
    for key in (
        "cash_collected_sar",
        "mrr_sar",
        "pipeline_sar",
        "weighted_pipeline_sar",
        "payment_followups_due",
        "source",
    ):
        assert key in body


def test_distribution_summary_endpoint(client: TestClient) -> None:
    res = client.get("/api/v1/internal/distribution/summary")
    assert res.status_code == 200
    body = res.json()
    for key in ("channels", "active_sectors", "experiments", "double_down", "source"):
        assert key in body


def test_delivery_retention_proof_queues(client: TestClient) -> None:
    for path in (
        "/api/v1/internal/delivery/queue",
        "/api/v1/internal/retention/queue",
        "/api/v1/internal/proof/library",
    ):
        res = client.get(path)
        assert res.status_code == 200
        assert isinstance(res.json(), list)


# ── Approval write endpoints ──────────────────────────────────────
def test_approve_a2_writes_audit_and_allows_external(
    client: TestClient, audit_log: Path
) -> None:
    res = client.post(
        "/api/v1/internal/approvals/apt-001/approve",
        json={
            "reason": "Founder approval, ICP fit confirmed",
            "approval_class": "A2",
            "risk_level": "Medium",
            "type": "outreach",
            "evidence": "scoring=0.82",
        },
    )
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["status"] == "Approved"
    assert body["policy_result"] == "ALLOW_AFTER_APPROVAL"
    assert body["external_action_allowed"] is True
    assert body["audit_written"] is True
    assert audit_log.exists()
    content = audit_log.read_text()
    assert "apt-001" in content
    assert "approve" in content
    assert "ALLOW_AFTER_APPROVAL" in content
    assert "scoring=0.82" in content


def test_approve_default_decision_is_accepted(client: TestClient) -> None:
    # decision field is optional; the endpoint infers approve.
    res = client.post(
        "/api/v1/internal/approvals/apt-009/approve",
        json={"reason": "ok"},
    )
    assert res.status_code == 200
    assert res.json()["status"] == "Approved"


def test_reject_writes_audit_and_blocks_external(
    client: TestClient, audit_log: Path
) -> None:
    res = client.post(
        "/api/v1/internal/approvals/apt-002/reject",
        json={"reason": "Off-ICP", "approval_class": "A2", "risk_level": "Low"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "Rejected"
    assert body["policy_result"] == "DENY"
    assert body["external_action_allowed"] is False
    assert "apt-002" in audit_log.read_text()


def test_request_edit_writes_audit_and_blocks_external(
    client: TestClient, audit_log: Path
) -> None:
    res = client.post(
        "/api/v1/internal/approvals/apt-003/request-edit",
        json={"reason": "Reword opening line", "approval_class": "A1"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "Needs Edit"
    assert body["policy_result"] == "NEEDS_EDIT"
    assert body["external_action_allowed"] is False
    assert "apt-003" in audit_log.read_text()


def test_a3_cannot_auto_execute_even_on_approve(client: TestClient) -> None:
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
    assert body["external_action_allowed"] is False
    assert "A3" in body["policy_result"]


def test_approve_rejects_mismatched_decision(client: TestClient) -> None:
    res = client.post(
        "/api/v1/internal/approvals/apt-005/approve",
        json={"decision": "reject", "approval_class": "A2"},
    )
    assert res.status_code == 400


def test_audit_appends_multiple_rows(client: TestClient, audit_log: Path) -> None:
    client.post(
        "/api/v1/internal/approvals/apt-006/approve",
        json={"reason": "first", "approval_class": "A1"},
    )
    client.post(
        "/api/v1/internal/approvals/apt-007/reject",
        json={"reason": "second", "approval_class": "A1"},
    )
    text = audit_log.read_text()
    # Header + 2 rows.
    assert text.count("\n") >= 3
    assert "apt-006" in text and "apt-007" in text


def test_write_audit_handles_unwritable_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The audit writer must not raise when the target is unwritable —
    the API still reports audit_written: False but the decision returns."""
    # Point the writer at a path under a *file* (not a directory) so
    # mkdir(..., parents=True) raises OSError without privilege tricks.
    blocker = tmp_path / "not-a-dir"
    blocker.write_text("x")
    monkeypatch.setattr(fc, "_AUDIT_LOG_PATH", blocker / "trust" / "log.csv")
    ok = fc._write_audit({"approval_id": "x", "decision": "approve"})
    assert ok is False

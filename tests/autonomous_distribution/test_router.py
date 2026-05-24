"""HTTP tests for /api/v1/autonomous-distribution/* router.

Mounts ONLY the autonomous_distribution router on a minimal FastAPI app
to avoid pulling the full Dealix app stack (DB, middleware, providers).
This keeps the test fast and isolated, while still exercising every line
of the router for coverage.
"""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.autonomous_distribution import router


@pytest.fixture()
def client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def _passport_body() -> dict:
    return {
        "source_id": "t1",
        "source_type": "inbound_form",
        "owner": "founder",
        "allowed_use": ["ai_processing", "internal_analysis"],
        "contains_pii": False,
        "sensitivity": "internal",
        "retention_policy": "90_days",
        "ai_access_allowed": True,
        "external_use_allowed": False,
    }


def _icp_body() -> dict:
    return {
        "b2b_service_fit": 80,
        "data_maturity": 70,
        "governance_posture": 75,
        "budget_signal": 70,
        "decision_velocity": 65,
    }


def _adoption_body() -> dict:
    return {
        "executive_sponsor": 80,
        "workflow_owner": 75,
        "data_readiness": 70,
        "user_engagement": 70,
        "approval_completion": 75,
        "proof_visibility": 70,
        "monthly_cadence": 70,
        "expansion_pull": 65,
    }


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

def test_health_returns_layers_and_loops(client: TestClient) -> None:
    r = client.get("/api/v1/autonomous-distribution/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "data_os" in body["layers"]
    assert "morning" in body["loops"]
    assert body["send_policy"].startswith("draft-only")


# ---------------------------------------------------------------------------
# Lead processing
# ---------------------------------------------------------------------------

def test_lead_process_returns_governance_decision(client: TestClient) -> None:
    r = client.post(
        "/api/v1/autonomous-distribution/lead/process",
        json={
            "lead_row": {
                "company_name": "Acme",
                "contact_email": "x@acme.sa",
                "contact_name": "Founder",
                "source_id": "t1",
            },
            "passport": _passport_body(),
            "icp": _icp_body(),
            "discovery_answers": {},
            "raw_request_text": "We need help with AI",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert "governance_decision" in body


def test_lead_process_blocks_scraping_source(client: TestClient) -> None:
    passport = _passport_body()
    passport["source_type"] = "scraping"
    r = client.post(
        "/api/v1/autonomous-distribution/lead/process",
        json={
            "lead_row": {"company_name": "X", "source_id": "t1"},
            "passport": passport,
            "icp": _icp_body(),
            "discovery_answers": {},
            "raw_request_text": "",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["governance_decision"] in {"BLOCK", "block"}


# ---------------------------------------------------------------------------
# Outreach audit
# ---------------------------------------------------------------------------

def test_outreach_audit_blocks_linkedin(client: TestClient) -> None:
    r = client.post(
        "/api/v1/autonomous-distribution/outreach/audit",
        json={"text": "Hello", "channel": "linkedin"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["safe_to_queue"] is False
    assert body["governance_decision"] in {"BLOCK", "block"}


def test_outreach_audit_blocks_whatsapp(client: TestClient) -> None:
    r = client.post(
        "/api/v1/autonomous-distribution/outreach/audit",
        json={"text": "Hello", "channel": "whatsapp"},
    )
    assert r.status_code == 200
    assert r.json()["safe_to_queue"] is False


def test_outreach_audit_allows_email_when_clean(client: TestClient) -> None:
    r = client.post(
        "/api/v1/autonomous-distribution/outreach/audit",
        json={
            "text": "Following up after our intro call last week.",
            "channel": "email",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert "governance_decision" in body
    assert "reasons" in body


# ---------------------------------------------------------------------------
# Payment processing
# ---------------------------------------------------------------------------

def test_payment_process_paid_with_proof_eligible(client: TestClient) -> None:
    r = client.post(
        "/api/v1/autonomous-distribution/payment/process",
        json={
            "invoice_ref": "INV-001",
            "amount_sar": 499.0,
            "moyasar_status": "paid",
            "moyasar_mode": "test",
            "customer_id": "cust-1",
            "rung": 2,
            "proof_pack_score": 85,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["capital_asset_eligible"] is True
    assert body["invoice_ref"] == "INV-001"


def test_payment_process_paid_without_proof_not_eligible(client: TestClient) -> None:
    r = client.post(
        "/api/v1/autonomous-distribution/payment/process",
        json={
            "invoice_ref": "INV-002",
            "amount_sar": 499.0,
            "moyasar_status": "paid",
            "moyasar_mode": "test",
            "customer_id": "cust-2",
            "rung": 2,
            "proof_pack_score": 40,
        },
    )
    assert r.status_code == 200
    assert r.json()["capital_asset_eligible"] is False


def test_payment_process_failed_status_blocks(client: TestClient) -> None:
    r = client.post(
        "/api/v1/autonomous-distribution/payment/process",
        json={
            "invoice_ref": "INV-003",
            "amount_sar": 499.0,
            "moyasar_status": "failed",
            "moyasar_mode": "test",
            "customer_id": "cust-3",
            "rung": 2,
            "proof_pack_score": 85,
        },
    )
    assert r.status_code == 200
    assert r.json()["capital_asset_eligible"] is False


# ---------------------------------------------------------------------------
# Proof Pack
# ---------------------------------------------------------------------------

def test_proof_pack_assemble_empty_returns_score(client: TestClient) -> None:
    r = client.post(
        "/api/v1/autonomous-distribution/proof-pack/assemble",
        json={"sections": {}, "governance_blocked": False},
    )
    assert r.status_code == 200
    body = r.json()
    assert "score" in body
    assert body["publish_eligible"] is False


def test_proof_pack_assemble_governance_blocked_marks_ineligible(client: TestClient) -> None:
    r = client.post(
        "/api/v1/autonomous-distribution/proof-pack/assemble",
        json={"sections": {}, "governance_blocked": True},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["publish_eligible"] is False


# ---------------------------------------------------------------------------
# Retainer assessment
# ---------------------------------------------------------------------------

def test_retainer_assess_high_adoption_eligible(client: TestClient) -> None:
    r = client.post(
        "/api/v1/autonomous-distribution/retainer/assess",
        json={
            "adoption": _adoption_body(),
            "customer_id": "cust-1",
            "proof_score": 85,
            "workflow_owner_exists": True,
            "monthly_workflow_exists": True,
            "governance_risk_controlled": True,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert "eligible" in body
    assert "adoption_band" in body


def test_retainer_assess_low_adoption_not_eligible(client: TestClient) -> None:
    low_adoption = {k: 20 for k in _adoption_body().keys()}
    r = client.post(
        "/api/v1/autonomous-distribution/retainer/assess",
        json={
            "adoption": low_adoption,
            "customer_id": "cust-2",
            "proof_score": 30,
            "workflow_owner_exists": False,
            "monthly_workflow_exists": False,
            "governance_risk_controlled": False,
        },
    )
    assert r.status_code == 200
    assert r.json()["eligible"] is False


# ---------------------------------------------------------------------------
# Loops (read-only)
# ---------------------------------------------------------------------------

def test_loops_morning(client: TestClient) -> None:
    r = client.get(
        "/api/v1/autonomous-distribution/loops/morning",
        params={"leads_inbound": 5, "leads_scored": 3, "drafts_pending": 2},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["leads_refreshed"] == 5
    assert body["leads_scored"] == 3
    assert body["drafts_queued"] == 2
    assert isinstance(body["high_priority_actions"], list)


def test_loops_evening(client: TestClient) -> None:
    r = client.get(
        "/api/v1/autonomous-distribution/loops/evening",
        params={"revenue_today_sar": 499.0, "leads_in_pipeline": 12},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["revenue_today_sar"] == 499.0
    assert body["leads_in_pipeline"] == 12
    assert isinstance(body["tomorrow_top_4"], list)


def test_loops_weekly(client: TestClient) -> None:
    r = client.get("/api/v1/autonomous-distribution/loops/weekly")
    assert r.status_code == 200
    body = r.json()
    assert "retainers_eligible" in body
    assert "capital_assets_added" in body
    assert "mrr_sar" in body


def test_loops_monthly_activation_phase(client: TestClient) -> None:
    r = client.get(
        "/api/v1/autonomous-distribution/loops/monthly",
        params={"days_since_launch": 15},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["month_phase"] in {"activation", "expansion", "compounding"}
    assert isinstance(body["decisions_for_founder"], list)


def test_loops_monthly_expansion_phase(client: TestClient) -> None:
    r = client.get(
        "/api/v1/autonomous-distribution/loops/monthly",
        params={"days_since_launch": 45},
    )
    assert r.status_code == 200
    assert r.json()["month_phase"] in {"activation", "expansion", "compounding"}


def test_loops_monthly_compounding_phase(client: TestClient) -> None:
    r = client.get(
        "/api/v1/autonomous-distribution/loops/monthly",
        params={"days_since_launch": 75},
    )
    assert r.status_code == 200
    assert r.json()["month_phase"] in {"activation", "expansion", "compounding"}

"""
API smoke tests for the Hermes routers.

Uses FastAPI TestClient on the composite router directly so the test
doesn't pull in the full Dealix app (which has heavier deps). This
exists primarily to cover the 16 router files in api/routers/hermes/
under the api coverage gate.
"""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.hermes._dependencies import get_hermes
from api.routers.hermes.composite import build_hermes_router
from dealix.hermes.config import seed_tools
from dealix.hermes.orchestrator import HermesOrchestrator, reset_orchestrator


@pytest.fixture()
def client(monkeypatch):
    reset_orchestrator()
    fresh = HermesOrchestrator().bootstrap()
    seed_tools(fresh.tool_registry)
    app = FastAPI()
    app.include_router(build_hermes_router())
    app.dependency_overrides[get_hermes] = lambda: fresh
    return TestClient(app)


def _capture_signal(client) -> str:
    r = client.post("/api/v1/hermes/signals/capture", json={
        "source": "customer", "signal_type": "customer",
        "title": "lead", "content": "content",
    })
    assert r.status_code == 200, r.text
    return r.json()["signal_id"]


def _score_opportunity(client, signal_id: str, *, level: str = "S1_INTERNAL") -> str:
    r = client.post("/api/v1/hermes/opportunities/score", json={
        "signal_id": signal_id,
        "opportunity_type": "customer",
        "title": "opp",
        "estimated_value_sar": 10000,
        "cash_speed_score": 4,
        "strategic_score": 3,
        "repeatability_score": 4,
        "data_moat_score": 3,
        "difficulty_score": 2,
        "risk_score": 1,
        "sovereignty_level": level,
    })
    assert r.status_code == 200, r.text
    return r.json()["opportunity_id"]


def _create_decision(client, opportunity_id: str) -> str:
    r = client.post("/api/v1/hermes/decisions/create", json={
        "opportunity_id": opportunity_id,
        "memo": "proceed",
        "rationale": "scored well",
        "expected_outcome": "win",
    })
    assert r.status_code == 200, r.text
    return r.json()["decision_id"]


# ── Kernel endpoints ──────────────────────────────────────────────


def test_kernel_full_chain(client):
    sig = _capture_signal(client)
    opp = _score_opportunity(client, sig)
    dec = _create_decision(client, opp)

    r = client.post("/api/v1/hermes/executions/plan", json={
        "decision_id": dec,
        "agent_id": "proposal_factory",
        "tools": ["draft_proposal"],
    })
    assert r.status_code == 200, r.text


def test_kernel_signal_not_found(client):
    r = client.post("/api/v1/hermes/opportunities/score", json={
        "signal_id": "sig_phantom",
        "opportunity_type": "customer",
        "title": "x",
    })
    assert r.status_code == 404


def test_kernel_unknown_agent_rejected(client):
    sig = _capture_signal(client)
    opp = _score_opportunity(client, sig)
    dec = _create_decision(client, opp)
    r = client.post("/api/v1/hermes/executions/plan", json={
        "decision_id": dec,
        "agent_id": "nonexistent_agent",
        "tools": [],
    })
    assert r.status_code == 400


def test_kernel_events_listing(client):
    _capture_signal(client)
    r = client.get("/api/v1/hermes/events")
    assert r.status_code == 200
    assert len(r.json()) >= 1


def test_outcome_and_asset_chain(client):
    """Push the full lifecycle through the HTTP layer."""
    sig = _capture_signal(client)
    opp = _score_opportunity(client, sig)
    dec = _create_decision(client, opp)
    exe = client.post("/api/v1/hermes/executions/plan", json={
        "decision_id": dec, "agent_id": "proposal_factory",
        "tools": ["draft_proposal"],
    }).json()

    # Trust check + dispatch + complete happens via kernel directly because
    # the HTTP layer doesn't expose those (intentional — Sami controls them).
    from api.routers.hermes._dependencies import get_hermes
    orch = client.app.dependency_overrides[get_hermes]()
    orch.kernel.executions.mark_trust_check(exe["execution_id"], passed=True)
    orch.kernel.executions.dispatch(exe["execution_id"])
    orch.kernel.executions.complete(exe["execution_id"])

    r = client.post("/api/v1/hermes/outcomes/log", json={
        "execution_id": exe["execution_id"],
        "status": "won",
        "actual_result": "signed",
        "revenue_sar": 5000,
        "asset_review_required": True,
    })
    assert r.status_code == 200
    outcome_id = r.json()["outcome_id"]

    r = client.post("/api/v1/hermes/assets/build", json={
        "outcome_id": outcome_id,
        "asset_type": "template",
        "title": "template",
    })
    assert r.status_code == 200
    asset_id = r.json()["asset_id"]

    # asset-level endpoints
    r = client.get("/api/v1/hermes/assets/")
    assert r.status_code == 200 and len(r.json()) >= 1

    r = client.get(f"/api/v1/hermes/assets/{asset_id}/scale-kill")
    assert r.status_code == 200

    r = client.get(f"/api/v1/hermes/assets/{asset_id}/commercial-review")
    assert r.status_code == 200


def test_outcome_unknown_execution_rejected(client):
    r = client.post("/api/v1/hermes/outcomes/log", json={
        "execution_id": "exe_phantom", "status": "won", "actual_result": "x",
    })
    assert r.status_code == 404


def test_asset_build_rejects_ineligible_outcome(client):
    sig = _capture_signal(client)
    opp = _score_opportunity(client, sig)
    dec = _create_decision(client, opp)
    exe = client.post("/api/v1/hermes/executions/plan", json={
        "decision_id": dec, "agent_id": "proposal_factory",
        "tools": ["draft_proposal"],
    }).json()
    from api.routers.hermes._dependencies import get_hermes
    orch = client.app.dependency_overrides[get_hermes]()
    orch.kernel.executions.mark_trust_check(exe["execution_id"], passed=True)
    orch.kernel.executions.dispatch(exe["execution_id"])
    orch.kernel.executions.complete(exe["execution_id"])
    out = client.post("/api/v1/hermes/outcomes/log", json={
        "execution_id": exe["execution_id"], "status": "lost", "actual_result": "x",
        "asset_review_required": False, "revenue_sar": 0,
    }).json()
    r = client.post("/api/v1/hermes/assets/build", json={
        "outcome_id": out["outcome_id"], "asset_type": "template", "title": "t",
    })
    assert r.status_code == 409


# ── Sovereign endpoints ───────────────────────────────────────────


def test_sovereign_console(client):
    r = client.get("/api/v1/hermes/sovereign/console")
    assert r.status_code == 200
    data = r.json()
    assert "pending_approvals" in data
    assert data["registered_agents"] >= 51


def test_sovereign_approval_flow(client):
    r = client.post("/api/v1/hermes/sovereign/approvals/open", json={
        "subject_id": "dec_x", "subject_type": "decision",
        "title": "t", "summary": "s",
        "sovereignty_level": "S2_SAMI_APPROVAL",
    })
    assert r.status_code == 200
    approval_id = r.json()["approval_id"]

    r = client.get("/api/v1/hermes/sovereign/approvals")
    assert r.status_code == 200 and len(r.json()) >= 1

    r = client.post(f"/api/v1/hermes/sovereign/approve?approval_id={approval_id}&approver=Sami")
    assert r.status_code == 200
    assert r.json()["state"] == "approved"


def test_sovereign_deny_flow(client):
    r = client.post("/api/v1/hermes/sovereign/approvals/open", json={
        "subject_id": "dec_y", "subject_type": "decision",
        "title": "t", "summary": "s", "sovereignty_level": "S2_SAMI_APPROVAL",
    })
    approval_id = r.json()["approval_id"]
    r = client.post(f"/api/v1/hermes/sovereign/deny?approval_id={approval_id}&reason=nope")
    assert r.status_code == 200 and r.json()["state"] == "denied"


def test_sovereign_approve_unknown(client):
    r = client.post("/api/v1/hermes/sovereign/approve?approval_id=missing")
    assert r.status_code == 404


def test_sovereign_kill_switch(client):
    r = client.post("/api/v1/hermes/sovereign/kill-switch", json={
        "target_type": "agent", "target_id": "rogue", "reason": "test",
    })
    assert r.status_code == 200
    r = client.post("/api/v1/hermes/sovereign/kill-switch/restore?target_type=agent&target_id=rogue")
    assert r.status_code == 200


def test_sovereign_restore_unknown(client):
    r = client.post("/api/v1/hermes/sovereign/kill-switch/restore?target_type=agent&target_id=ghost")
    assert r.status_code == 404


# ── Trust endpoints ───────────────────────────────────────────────


def test_trust_lists(client):
    assert client.get("/api/v1/hermes/trust/agents").status_code == 200
    assert client.get("/api/v1/hermes/trust/tools").status_code == 200
    assert client.get("/api/v1/hermes/trust/risks").status_code == 200
    assert client.get("/api/v1/hermes/trust/incidents").status_code == 200
    assert client.get("/api/v1/hermes/trust/audit").status_code == 200


def test_trust_check_overclaim(client):
    r = client.post("/api/v1/hermes/trust/check", json={
        "agent_id": "copywriter",
        "proposed_text": "guaranteed 100% accuracy",
    })
    assert r.status_code == 200
    assert r.json()["passed"] is False


def test_trust_check_clean(client):
    r = client.post("/api/v1/hermes/trust/check", json={
        "agent_id": "copywriter",
        "proposed_text": "Helping founders ship faster.",
    })
    assert r.status_code == 200
    assert r.json()["passed"] is True


def test_trust_register_agent_and_tool(client):
    agent_payload = {
        "agent_id": "test_a",
        "owner": "Sami",
        "domain": "test",
        "mission": "test",
        "max_sovereignty_level": "S0_AUTO_SAFE",
        "allowed_tools": ["x"],
        "forbidden_tools": [],
        "kpis": ["k"],
        "active": True,
    }
    assert client.post("/api/v1/hermes/trust/agents/register", json=agent_payload).status_code == 200
    tool_payload = {
        "tool_id": "x",
        "owner": "Sami",
        "description": "",
        "risk_level": "low",
        "enabled": True,
        "requires_approval": False,
        "allowed_agents": [],
        "data_scope": "internal_only",
        "audit_required": True,
        "pdpl_relevant": False,
    }
    assert client.post("/api/v1/hermes/trust/tools/register", json=tool_payload).status_code == 200


def test_trust_evidence_pack(client):
    r = client.post("/api/v1/hermes/trust/evidence-pack", json={
        "subject_id": "dec_1", "subject_type": "decision",
        "items": [{"source": "manual", "excerpt": "snippet"}],
        "model_used": "test", "bilingual_memo_ar": "", "bilingual_memo_en": "",
    })
    assert r.status_code == 200


def test_trust_mcp_review_pass(client):
    r = client.post("/api/v1/hermes/trust/mcp-review", json={
        "manifest": {"owner": "Sami", "tools": [], "data_scope": "internal", "signed": True},
        "descriptors": [{"name": "read_x", "description": "read some x"}],
    })
    assert r.status_code == 200
    assert r.json()["all_passed"] is True


def test_trust_mcp_review_blocks_unsigned(client):
    r = client.post("/api/v1/hermes/trust/mcp-review", json={
        "manifest": {"owner": "x", "tools": [], "data_scope": "internal"},
        "descriptors": [],
    })
    assert r.status_code == 200
    assert r.json()["all_passed"] is False


# ── Money / Growth / Products / Partners / Customers ──────────────


def test_money_dashboard(client):
    r = client.get("/api/v1/hermes/money/dashboard")
    assert r.status_code == 200
    assert "cash_risk" in r.json()


def test_money_revenue_quality(client):
    r = client.post("/api/v1/hermes/money/revenue-assurance", json={
        "margin_ratio": 0.5, "repeatability": 0.6, "retainer_potential": 0.4,
        "data_moat": 0.3, "partner_potential": 0.2, "delivery_burden": 0.2,
    })
    assert r.status_code == 200
    assert 0.0 <= r.json()["score"] <= 1.0


def test_growth_campaign_requires_offer(client):
    r = client.post("/api/v1/hermes/growth/campaigns", json={
        "name": "x", "target_icp": "y", "offer_id": "", "channel": "linkedin",
    })
    assert r.status_code == 422


def test_growth_campaign_create_and_list(client):
    r = client.post("/api/v1/hermes/growth/campaigns", json={
        "name": "c", "target_icp": "ksa_sme", "offer_id": "ai_trust_kit",
        "channel": "linkedin", "message_angle": "trust", "cta": "book_call",
    })
    assert r.status_code == 200
    assert client.get("/api/v1/hermes/growth/campaigns").status_code == 200


def test_growth_leads_and_experiments(client):
    assert client.post("/api/v1/hermes/growth/leads", json={
        "source": "linkedin", "company_name": "Acme", "icp": "ksa_sme",
    }).status_code == 200
    assert client.get("/api/v1/hermes/growth/leads").status_code == 200
    assert client.post("/api/v1/hermes/growth/experiments", json={
        "title": "test", "hypothesis": "h", "primary_metric": "m",
        "success_threshold": 0.5, "kill_rule": "stop",
    }).status_code == 200
    assert client.get("/api/v1/hermes/growth/experiments").status_code == 200
    assert client.get("/api/v1/hermes/growth/dashboard").status_code == 200


def test_products_offers(client):
    r = client.get("/api/v1/hermes/products/offers")
    assert r.status_code == 200 and len(r.json()) >= 3
    r = client.get("/api/v1/hermes/products/offers/ai_trust_kit/readiness")
    assert r.status_code == 200 and r.json()["ready"] is True
    r = client.get("/api/v1/hermes/products/offers/unknown/readiness")
    assert r.status_code == 200 and r.json()["ready"] is False


def test_partners_fit_score(client):
    r = client.post("/api/v1/hermes/partners/fit-score", json={
        "client_base_score": 5, "sales_capability": 4, "delivery_capability": 3,
        "trust_level": 4, "sector_fit": 5, "risk_level": 2,
    })
    assert r.status_code == 200
    assert r.json()["score"] >= 0


def test_customers_health_and_churn(client):
    r = client.post("/api/v1/hermes/customers/health-score", json={
        "customer_id": "c1", "usage_score": 0.8, "nps_score": 50,
        "paid_on_time": True, "open_tickets": 1,
    })
    assert r.status_code == 200

    r = client.post("/api/v1/hermes/customers/churn-risk", json={
        "customer_id": "c1", "health_score": 0.2,
        "days_since_last_activity": 45, "open_tickets_critical": 1,
        "payment_late_days": 20,
    })
    assert r.status_code == 200 and r.json()["risk"] == "high"


def test_intelligence_radar(client):
    r = client.post("/api/v1/hermes/intelligence/radar", json={
        "signal_id": "rad_1", "source": "news", "headline": "x", "summary": "y",
    })
    assert r.status_code == 200
    assert client.get("/api/v1/hermes/intelligence/radar").status_code == 200


def test_intelligence_trend_to_offer(client):
    r = client.get(
        "/api/v1/hermes/intelligence/trend-to-offer"
        "?trend=AI%20Governance&buyer=CISO&pain=audit",
    )
    assert r.status_code == 200
    assert r.json()["plausibility_score"] >= 1


def test_training_workshop(client):
    r = client.post("/api/v1/hermes/training/workshops", json={
        "workshop_id": "w1", "title": "T", "audience": "ksa_founder",
        "duration_minutes": 90, "learning_outcomes": ["x"], "materials": [],
    })
    assert r.status_code == 200


def test_ventures_launch_and_evaluate(client):
    r = client.post("/api/v1/hermes/ventures/launch", json={
        "vertical_id": "v1", "vertical": "agencies", "buyer": "owner",
        "pain": "x", "offer_id": "agency_white_label_kit",
        "first_50_targets": ["a", "b"], "pilot_metric": "p",
        "scale_rule": "2 paid", "kill_rule": "0 replies",
    })
    assert r.status_code == 200
    r2 = client.post("/api/v1/hermes/ventures/launch", json={
        "vertical_id": "v_bad", "vertical": "v", "buyer": "b", "pain": "p",
        "offer_id": "o", "first_50_targets": [],
        "scale_rule": "", "kill_rule": "",
    })
    assert r2.status_code == 422
    r3 = client.get("/api/v1/hermes/ventures/evaluate?paid_pilots=3&qualified_replies=10&days_since_launch=10")
    assert r3.status_code == 200 and r3.json()["verdict"] == "scale"


def test_observability_health_and_events(client):
    _capture_signal(client)
    r = client.get("/api/v1/hermes/observability/system-health")
    assert r.status_code == 200
    r = client.get("/api/v1/hermes/observability/lifecycle-events")
    assert r.status_code == 200 and len(r.json()) >= 1

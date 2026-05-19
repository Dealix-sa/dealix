"""Executive Orchestrator — the autonomous top of the agent pyramid.

Covers: aggregation + degradation, decision ranking, the queues-never-sends
guarantee, autonomy ceiling, audit coverage, canonical action types, the
safety preflight (kill switch + doctrine), dry-run, capped auto-spawn, the
API surface, and the founder dashboard section.
"""

from __future__ import annotations

import asyncio

import pytest
from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.agent_os import (
    clear_for_test as clear_agents,
)
from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.approval_center.schemas import (
    ApprovalStatus,
    is_canonical_action_type,
)
from auto_client_acquisition.auditability_os.audit_event import (
    clear_for_test as clear_audit,
)
from auto_client_acquisition.auditability_os.audit_event import list_events
from auto_client_acquisition.executive_os import (
    GUARDRAILS,
    aggregator_degraded_roles,
    build_all_role_briefs,
    build_executive_agent_card,
    run_executive_tick,
    spawn_internal_jobs,
)
from auto_client_acquisition.executive_os import (
    clear_for_test as clear_briefs,
)
from auto_client_acquisition.executive_os.orchestrator import _prepare_internal_jobs
from auto_client_acquisition.executive_os.schemas import RankedDecision
from auto_client_acquisition.secure_agent_runtime_os import (
    activate_kill_switch,
    reset_kill_switch_for_tests,
)

client = TestClient(app)

_CANONICAL = {
    "prepare_diagnostic",
    "draft_email",
    "draft_linkedin_manual",
    "call_script",
    "follow_up_task",
    "support_reply_draft",
    "payment_reminder",
    "delivery_task",
    "proof_request",
    "upsell_recommendation",
    "partner_intro",
}


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_AGENT_REGISTRY_PATH", str(tmp_path / "agents.jsonl"))
    monkeypatch.setenv("DEALIX_AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    monkeypatch.setenv("DEALIX_EXECUTIVE_BRIEF_PATH", str(tmp_path / "exec.jsonl"))
    monkeypatch.setenv("DEALIX_EXECUTIVE_ORCHESTRATOR_ENABLED", "false")
    _reset()
    yield
    _reset()


def _reset() -> None:
    from core.config.settings import get_settings

    clear_agents()
    get_default_approval_store().clear()
    reset_kill_switch_for_tests()
    clear_briefs()
    clear_audit()
    get_settings.cache_clear()


def _set_flag(monkeypatch, value: bool) -> None:
    from core.config.settings import get_settings

    monkeypatch.setenv("DEALIX_EXECUTIVE_ORCHESTRATOR_ENABLED", "true" if value else "false")
    get_settings.cache_clear()


# ── Aggregation ──────────────────────────────────────────────────


def test_aggregator_returns_all_seven_roles():
    briefs = build_all_role_briefs()
    assert set(briefs) == {"ceo", "sales", "growth", "partnership", "cs", "finance", "compliance"}


def test_aggregator_degrades_without_crashing(monkeypatch):
    import auto_client_acquisition.executive_os.aggregator as agg

    real = agg.build_role_brief

    def _flaky(role):
        if role.value == "finance":
            raise RuntimeError("boom")
        return real(role)

    monkeypatch.setattr(agg, "build_role_brief", _flaky)
    briefs = build_all_role_briefs()
    assert briefs["finance"] is None
    assert "finance" in aggregator_degraded_roles(briefs)
    assert briefs["ceo"] is not None


# ── Synthesis ────────────────────────────────────────────────────


def test_decisions_ranked_by_risk():
    result = run_executive_tick()
    assert result.ok and result.brief is not None
    order = {"blocked": 0, "high": 1, "medium": 2, "low": 3}
    ranks = [order.get(d.risk_level, 3) for d in result.brief.ranked_decisions]
    assert ranks == sorted(ranks)


def test_action_types_are_canonical():
    result = run_executive_tick()
    assert result.brief is not None
    for decision in result.brief.ranked_decisions:
        assert decision.action_type in _CANONICAL
        assert is_canonical_action_type(decision.action_type)


def test_one_number_counts_approval_required():
    result = run_executive_tick()
    brief = result.brief
    assert brief is not None
    expected = sum(1 for d in brief.ranked_decisions if d.approval_required)
    assert brief.one_number_that_matters == expected


# ── Queues, never sends ──────────────────────────────────────────


def test_queues_never_sends():
    result = run_executive_tick()
    assert result.brief is not None
    for queued in result.brief.queued_approvals:
        assert queued.action_mode != "approved_execute"
        assert queued.action_mode in {"draft_only", "approval_required", "blocked"}
    # Nothing in the store was ever approved by the orchestrator.
    history = get_default_approval_store().list_history(limit=500)
    assert all(ApprovalStatus(r.status) != ApprovalStatus.APPROVED for r in history)


def test_autonomy_capped_at_l3_with_no_tools():
    card = build_executive_agent_card()
    assert card.autonomy_level == 3
    assert card.allowed_tools == ()
    assert card.kill_switch_owner == "founder"


def test_every_queued_decision_is_audited():
    result = run_executive_tick()
    assert result.brief is not None
    events = list_events(customer_id="__executive__")
    assert len(events) >= len(result.brief.queued_approvals) + 1
    assert all(e.kind == "governance_decision" for e in events)
    assert all(e.actor == "executive_orchestrator" for e in events)


# ── Safety preflight ─────────────────────────────────────────────


def test_kill_switch_aborts_and_queues_nothing():
    activate_kill_switch()
    result = run_executive_tick()
    assert result.ok is False
    assert result.aborted_at == "kill_switch"
    assert result.brief is None
    assert get_default_approval_store().list_history(limit=500) == []


def test_doctrine_breach_aborts_tick(monkeypatch):
    import auto_client_acquisition.executive_os.orchestrator as orch

    def _raise():
        raise ValueError("doctrine breach")

    monkeypatch.setattr(orch, "enforce_doctrine_non_negotiables", _raise)
    result = run_executive_tick()
    assert result.ok is False
    assert "ValueError" in result.reason
    assert get_default_approval_store().list_history(limit=500) == []


def test_dry_run_queues_nothing():
    result = run_executive_tick(dry_run=True)
    assert result.ok is True
    assert result.reason == "dry_run"
    assert result.brief is not None
    assert get_default_approval_store().list_history(limit=500) == []
    assert list_events(customer_id="__executive__") == []


# ── Auto-spawn ───────────────────────────────────────────────────


def test_auto_spawn_is_capped_at_five():
    sales_decisions = [
        RankedDecision(
            role="sales",
            rank=i,
            title_ar="ع",
            title_en="x",
            risk_level="medium",
            approval_required=True,
        )
        for i in range(1, 9)
    ]
    jobs = _prepare_internal_jobs(sales_decisions)
    assert len(jobs) == 5
    assert all(j["job_type"] == "proposal_draft" for j in jobs)


def test_spawn_tolerates_absent_redis(monkeypatch):
    def _no_pool(*_a, **_k):
        raise ConnectionError("no redis here")

    monkeypatch.setattr("arq.create_pool", _no_pool)
    jobs = [{"job_type": "proposal_draft", "status": "prepared", "payload": {}}]
    spawned = asyncio.run(spawn_internal_jobs(jobs))
    assert len(spawned) == 1
    assert spawned[0]["status"] == "deferred"


# ── API surface ──────────────────────────────────────────────────


def test_status_endpoint_declares_guardrails():
    resp = client.get("/api/v1/executive/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["autonomy_level"] == 3
    assert body["guardrails"] == GUARDRAILS
    assert all(body["guardrails"].values())


def test_brief_endpoint_happy_path():
    empty = client.get("/api/v1/executive/brief")
    assert empty.status_code == 200
    assert empty.json()["data_status"] == "no_brief_yet"

    run_executive_tick()
    after = client.get("/api/v1/executive/brief")
    assert after.status_code == 200
    body = after.json()
    assert body["data_status"] == "ok"
    assert "headline_en" in body["brief"]


def test_tick_returns_404_when_flag_off():
    # Pass the admin gate (dev mode: any non-empty key) so the flag
    # check — not the auth check — is what produces the response.
    resp = client.post(
        "/api/v1/executive/tick",
        headers={"X-Admin-API-Key": "dev"},
    )
    assert resp.status_code == 404


def test_tick_is_admin_gated(monkeypatch):
    _set_flag(monkeypatch, True)
    monkeypatch.setenv("ADMIN_API_KEYS", "secret-admin-key")

    denied = client.post("/api/v1/executive/tick?dry_run=true")
    assert denied.status_code == 403

    allowed = client.post(
        "/api/v1/executive/tick?dry_run=true",
        headers={"X-Admin-API-Key": "secret-admin-key"},
    )
    assert allowed.status_code == 200
    assert allowed.json()["ok"] is True


# ── Founder dashboard integration ────────────────────────────────


def test_beast_command_center_includes_executive_section():
    from api.routers.founder_beast_command_center import _build_payload

    run_executive_tick()
    payload = _build_payload()
    assert "executive_brief" in payload
    assert payload["executive_brief"]["data_status"] == "ok"


def test_beast_command_center_executive_section_degrades(monkeypatch):
    import api.routers.founder_beast_command_center as bcc

    def _raise():
        raise RuntimeError("brief store down")

    monkeypatch.setattr(bcc, "_executive_brief", _raise)
    payload = bcc._build_payload()
    assert "executive_brief" in payload
    assert payload["degraded"] is True

"""Tests for the Dealix Autonomous Growth & Strategy Execution OS.

These assert the safety-critical guarantees: draft-only, approval-first,
forbidden actions blocked, external channels never auto-executed, and a full
orchestrator cycle producing only reviewable artifacts.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from dealix.autonomous_os import (
    ApprovalQueue,
    ApprovalState,
    AutonomousOS,
    ModelRouter,
    SafetyGate,
    StrategyRegistry,
    integrations,
)
from dealix.autonomous_os.adapters import all_status
from dealix.autonomous_os.adapters.calcom_adapter import CalComAdapter
from dealix.autonomous_os.adapters.firecrawl_adapter import FirecrawlAdapter
from dealix.autonomous_os.adapters.ollama_adapter import OllamaAdapter
from dealix.autonomous_os.adapters.twenty_adapter import TwentyCRMAdapter
from dealix.autonomous_os.adapters.whatsapp_draft_adapter import WhatsAppDraftAdapter
from dealix.autonomous_os.draft_composer import DraftComposer
from dealix.autonomous_os.execution_planner import ExecutionPlanner
from dealix.autonomous_os.growth_engine import GrowthContext, GrowthEngine
from dealix.autonomous_os.safety_gate import Route


# --------------------------- SafetyGate -----------------------------------
def test_gate_blocks_forbidden_actions():
    gate = SafetyGate(env={})
    for action in ("cold_outreach", "mass_send", "linkedin_automation", "auto_invoice"):
        decision = gate.evaluate(action=action)
        assert decision.route == Route.BLOCKED, action
        assert decision.blocked


def test_gate_routes_external_channels_to_approval():
    gate = SafetyGate(env={})
    for channel in ("whatsapp", "email", "sms", "linkedin"):
        decision = gate.evaluate(action="draft_followup", channel=channel, risk=0.1)
        assert decision.route == Route.APPROVAL, channel
        assert not decision.allowed_auto


def test_gate_high_risk_needs_approval():
    gate = SafetyGate(env={})
    assert gate.evaluate(action="draft_x", risk=0.4).route == Route.APPROVAL
    assert gate.evaluate(action="draft_x", risk=0.1).route == Route.AUTO_DRAFT


def test_gate_low_risk_internal_auto_draft():
    gate = SafetyGate(env={})
    decision = gate.evaluate(action="draft_proof_pack", kind="internal", risk=0.1)
    assert decision.route == Route.AUTO_DRAFT
    assert decision.allowed_auto


def test_gate_tripwire_raises_on_unsafe_env():
    unsafe = SafetyGate(env={"EXTERNAL_SEND_ENABLED": "true", "OUTBOUND_MODE": "draft_only"})
    with pytest.raises(RuntimeError):
        unsafe.assert_draft_only()


def test_gate_tripwire_ok_when_draft_only():
    SafetyGate(env={"OUTBOUND_MODE": "draft_only"}).assert_draft_only()  # no raise


# --------------------------- Registry -------------------------------------
def test_registry_loads_shipped_strategies():
    reg = StrategyRegistry().load()
    ids = {s.id for s in reg.all()}
    assert {"revenue_sprint", "saudi_market_access", "technical_trust"}.issubset(ids)
    # active() sorted by priority desc
    active = reg.active()
    assert active[0].priority >= active[-1].priority


def test_registry_rejects_duplicate_ids(tmp_path: Path):
    d = tmp_path / "s"
    d.mkdir()
    (d / "a.yaml").write_text("id: dup\nname: A\nsteps: []\n", encoding="utf-8")
    (d / "b.yaml").write_text("id: dup\nname: B\nsteps: []\n", encoding="utf-8")
    with pytest.raises(ValueError):
        StrategyRegistry(strategies_dir=d).load()


# --------------------------- Planner --------------------------------------
def test_planner_routes_revenue_sprint():
    reg = StrategyRegistry().load()
    planner = ExecutionPlanner(SafetyGate(env={}))
    plan = planner.plan(reg.get("revenue_sprint"))
    # internal low-risk drafts auto, whatsapp follow-up to approval
    assert len(plan.auto_steps) >= 2
    assert len(plan.approval_steps) >= 1
    assert all(s.channel != "whatsapp" for s in plan.auto_steps)


# --------------------------- Growth engine --------------------------------
def test_growth_engine_prioritises_proof_to_sprint():
    recs = GrowthEngine().recommend(GrowthContext(proof_assets_ready=3, booked_sprints=0))
    assert recs[0].offer == "transformation_diagnostic_sprint"
    assert recs[0].priority == 95


def test_growth_engine_always_returns_internal_content_action():
    recs = GrowthEngine().recommend(GrowthContext())
    assert any(r.kind == "internal" for r in recs)


# --------------------------- Model router ---------------------------------
def test_router_prefers_local_when_available():
    r = ModelRouter(env={"OLLAMA_HOST": "http://localhost:11434"})
    choice = r.route("strategy")
    assert choice.is_local
    assert choice.provider == "ollama"


def test_router_falls_back_to_hosted_when_no_local():
    r = ModelRouter(env={"DEEPSEEK_API_KEY": "present"})
    choice = r.route("draft")
    assert not choice.is_local
    assert choice.provider == "deepseek"
    assert "present" not in choice.endpoint  # never leaks the secret value


def test_router_default_is_local_target():
    choice = ModelRouter(env={}).route("default")
    assert choice.is_local  # deterministic local target for planning


# --------------------------- Approval queue -------------------------------
def test_approval_queue_submit_and_decide(tmp_path: Path):
    q = ApprovalQueue(tmp_path)
    item = q.submit(
        strategy_id="revenue_sprint",
        action="prepare_followup_drafts",
        draft="draft body",
        reason="external channel",
        channel="whatsapp",
    )
    assert len(q.list_pending()) == 1
    assert q.decide(item.id, approved=True, decided_by="founder")
    assert q.list_pending() == []
    assert q.stats()[ApprovalState.APPROVED.value] == 1


# --------------------------- Integrations ---------------------------------
def test_integrations_registry_is_honest():
    summ = integrations.summary()
    assert summ["total"] >= 40
    # Exactly the adapters that have real code are marked wired.
    wired = {i.name for i in integrations.by_status("wired")}
    assert wired == {"ollama", "twenty", "evolution_api", "firecrawl", "calcom"}
    assert "ollama" in summ["core_stack"]


# --------------------------- Adapters -------------------------------------
def test_ollama_adapter_offline_fallback_never_raises():
    ad = OllamaAdapter(env={})  # not configured -> offline
    assert not ad.is_available()
    res = ad.generate("draft a short note", model="llama3.1")
    assert res.ok
    assert res.mode == "offline_fallback"
    assert "DRAFT" in res.data


def test_ollama_adapter_bad_host_degrades_gracefully():
    # Configured but unreachable host must fall back, not raise.
    ad = OllamaAdapter(env={"OLLAMA_HOST": "http://127.0.0.1:0"})
    res = ad.generate("hi", model="llama3.1")
    assert res.ok
    assert res.mode == "offline_fallback"


def test_twenty_adapter_offline_returns_zero_context():
    ad = TwentyCRMAdapter(env={})
    res = ad.fetch_growth_context()
    assert res.ok and res.mode == "offline_fallback"
    assert res.data["warm_leads"] == 0


def test_twenty_adapter_reads_local_snapshot(tmp_path):
    snap = tmp_path / "crm_context.json"
    snap.write_text('{"warm_leads": 7, "proof_assets_ready": 2}', encoding="utf-8")
    ad = TwentyCRMAdapter(env={}, local_snapshot=snap)
    res = ad.fetch_growth_context()
    assert res.data["warm_leads"] == 7
    assert res.data["proof_assets_ready"] == 2


def test_whatsapp_adapter_has_no_send_capability():
    ad = WhatsAppDraftAdapter(env={})
    # Provably no send method exists anywhere on the adapter.
    for attr in dir(ad):
        assert "send" not in attr.lower(), attr


def test_whatsapp_draft_is_never_sendable():
    ad = WhatsAppDraftAdapter(env={})
    res = ad.build_draft(to_label="account:x", message="hello", consent_confirmed=True)
    assert res.data["will_send"] is False
    assert res.data["requires_founder_approval"] is True


def test_whatsapp_draft_blocked_without_consent():
    ad = WhatsAppDraftAdapter(env={})
    res = ad.build_draft(to_label="account:x", message="hello", consent_confirmed=False)
    assert res.data["status"] == "blocked"
    assert res.data["will_send"] is False


def test_draft_composer_offline_produces_draft():
    composed = DraftComposer(env={}).compose(
        action="draft_sprint_proposal", strategy_id="revenue_sprint", language="ar"
    )
    assert composed["is_draft"] and composed["will_send"] is False
    assert composed["draft_text"]


def test_all_status_reports_all_adapters():
    statuses = all_status(env={})
    names = {s["name"] for s in statuses}
    assert names == {"ollama", "twenty_crm", "whatsapp_draft", "firecrawl", "calcom"}
    wa = next(s for s in statuses if s["name"] == "whatsapp_draft")
    assert wa["mode"] == "draft_only"


def test_firecrawl_refuses_social_and_contact_sources():
    fc = FirecrawlAdapter(env={"FIRECRAWL_API_KEY": "x"})
    blocked = fc.scrape("https://www.linkedin.com/in/someone")
    assert not blocked.ok and blocked.mode == "blocked"
    q = fc.guard_query("find personal email of CFO")
    assert not q.ok and q.mode == "blocked"


def test_firecrawl_allows_public_research_query_and_offline():
    fc = FirecrawlAdapter(env={})  # not configured
    assert fc.guard_query("Saudi logistics sector trends 2026").ok
    res = fc.scrape("https://example.com/market-report")
    assert res.ok and res.mode == "offline_fallback"


def test_calcom_offline_returns_booking_link_no_booking():
    cal = CalComAdapter(env={"CALCOM_BOOKING_URL": "https://cal.com/dealix"})
    res = cal.booking_link("diagnostic")
    assert res.ok
    assert res.data["creates_booking"] is False
    assert res.data["booking_url"].endswith("/diagnostic")


# --------------------------- Full orchestrator ----------------------------
def test_orchestrator_full_cycle_is_draft_only(tmp_path: Path):
    os_engine = AutonomousOS(runtime_root=tmp_path, env={"OUTBOUND_MODE": "draft_only"})
    summary = os_engine.run(growth_context={"proof_assets_ready": 2, "warm_leads": 5})

    assert summary["mode"] == "draft_only"
    assert summary["counters"]["drafted"] >= 1
    assert summary["counters"]["approval"] >= 1
    # Reports written.
    report_dir = tmp_path / "reports"
    assert any(report_dir.glob("autonomous-os-*.md"))
    assert any(report_dir.glob("autonomous-os-*.json"))
    # Proof trail exists and records a completed run.
    events = os_engine.proofs.read_all()
    assert any(e["event_type"] == "run_completed" for e in events)
    # Approval queue has real pending items; nothing was "sent".
    assert os_engine.approvals.stats()["pending"] >= 1
    # Adapters status surfaced; nothing claims to be sending.
    assert {a["name"] for a in summary["adapters"]} == {
        "ollama",
        "twenty_crm",
        "whatsapp_draft",
        "firecrawl",
        "calcom",
    }
    # A WhatsApp external step carries a provably-unsendable draft payload.
    pending = os_engine.approvals.list_pending()
    wa_items = [p for p in pending if p.get("channel") == "whatsapp"]
    assert wa_items, "expected at least one whatsapp approval item"
    assert wa_items[0]["payload"]["whatsapp_draft"]["will_send"] is False


def test_orchestrator_blocks_forbidden_strategy_step(tmp_path: Path):
    strat_dir = tmp_path / "strategies"
    strat_dir.mkdir()
    (strat_dir / "bad.yaml").write_text(
        "id: bad\nname: Bad\nenabled: true\npriority: 10\nsteps:\n"
        "  - action: cold_outreach\n    kind: external_draft\n    risk: 0.9\n",
        encoding="utf-8",
    )
    os_engine = AutonomousOS(
        runtime_root=tmp_path / "rt", strategies_dir=strat_dir, env={"OUTBOUND_MODE": "draft_only"}
    )
    summary = os_engine.run()
    assert summary["counters"]["blocked"] == 1
    assert summary["counters"]["approval"] == 0
    # Nothing forbidden reached the approval queue.
    assert os_engine.approvals.stats()["pending"] == 0


def test_runtime_outputs_are_json_serialisable(tmp_path: Path):
    os_engine = AutonomousOS(runtime_root=tmp_path, env={"OUTBOUND_MODE": "draft_only"})
    summary = os_engine.run()
    json.dumps(summary)  # must not raise

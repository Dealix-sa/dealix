"""
Sovereign Control Plane — §81–§110 coverage tests.

Every public surface added by ``dealix/sovereign_control_plane/`` has
at least one test here. Tests are short, deterministic, and depend on
nothing outside ``dealix/``.
"""

from __future__ import annotations

import json

import pytest

from dealix.sovereign_control_plane import get_control_plane
from dealix.sovereign_control_plane.agent_runtime import AgentRuntime
from dealix.sovereign_control_plane.approvals import SovereignApprovalCenter
from dealix.sovereign_control_plane.assets import AssetLibrary
from dealix.sovereign_control_plane.classification import (
    Classifier,
    is_agent_ingest_allowed,
    is_export_allowed,
)
from dealix.sovereign_control_plane.context_feed import ContextFeedEngine
from dealix.sovereign_control_plane.customer_loop import CustomerValueLoop
from dealix.sovereign_control_plane.events import EventBus, make_event
from dealix.sovereign_control_plane.hermes import HermesOrchestrator
from dealix.sovereign_control_plane.identity import IdentityRegistry
from dealix.sovereign_control_plane.incidents import IncidentLog
from dealix.sovereign_control_plane.intelligence_graph import IntelligenceGraph
from dealix.sovereign_control_plane.marketplace import MarketplaceReadiness
from dealix.sovereign_control_plane.mcp_gateway import (
    MCPGateway,
    MCPServerDescriptor,
    manifest_hash_of,
)
from dealix.sovereign_control_plane.memory import MemoryKind, MemoryManager
from dealix.sovereign_control_plane.money_command import Deal, MoneyCommand
from dealix.sovereign_control_plane.offers import Offer, OfferGateError, OfferRegistry
from dealix.sovereign_control_plane.packaging import recommend_offer_tier
from dealix.sovereign_control_plane.partner_loop import PartnerValueLoop
from dealix.sovereign_control_plane.policy import PolicyEngine
from dealix.sovereign_control_plane.public_api import PublicAPIReadiness
from dealix.sovereign_control_plane.security_modes import SecurityModeManager
from dealix.sovereign_control_plane.tool_gateway import (
    HermesToolGateway,
    ToolDescriptor,
    ToolRegistry,
)
from dealix.sovereign_control_plane.tool_runtime import ToolRuntimeLog
from dealix.sovereign_control_plane.types import (
    ApprovalDecision,
    DataSensitivity,
    IdentityKind,
    IncidentSeverity,
    IncidentType,
    OfferState,
    RiskLevel,
    RunStatus,
    SecurityMode,
    SovereigntyLevel,
    ToolCallStatus,
    WorkspaceType,
)
from dealix.sovereign_control_plane.venture_loop import VentureValueLoop
from dealix.sovereign_control_plane.workspace import WorkspaceRegistry


# ─── Identity ────────────────────────────────────────────────────
def test_identity_agent_cannot_override_sami() -> None:
    reg = IdentityRegistry()
    sami = reg.register_sami()
    agent = reg.register(IdentityKind.AGENT, "hermes")
    assert reg.can_override(agent.identity_id, sami.identity_id) is False
    assert reg.can_override(sami.identity_id, agent.identity_id) is True


def test_identity_tool_cannot_override_sami() -> None:
    reg = IdentityRegistry()
    sami = reg.register_sami()
    tool = reg.register(IdentityKind.TOOL, "send_email")
    assert reg.can_override(tool.identity_id, sami.identity_id) is False
    assert reg.rank_of(sami.identity_id) > reg.rank_of(tool.identity_id)


# ─── Workspace ────────────────────────────────────────────────────
def test_workspace_bootstrap_creates_one_per_kind() -> None:
    ids = IdentityRegistry()
    sami = ids.register_sami()
    ws = WorkspaceRegistry()
    created = ws.bootstrap(sami.identity_id)
    assert len(created) == len(list(WorkspaceType))
    assert ws.get_by_kind(WorkspaceType.SOVEREIGN).sensitivity_level == DataSensitivity.SOVEREIGN


# ─── Classification ──────────────────────────────────────────────
def test_classifier_sovereign_export_blocked() -> None:
    c = Classifier()
    item = c.classify("sovereign decision: lockdown plan")
    assert item.sensitivity == DataSensitivity.SOVEREIGN
    assert is_export_allowed(DataSensitivity.SOVEREIGN) is False
    assert is_agent_ingest_allowed(DataSensitivity.SOVEREIGN) is False
    assert json.dumps(item.to_dict())


def test_classifier_default_public() -> None:
    c = Classifier()
    item = c.classify("nice weather today")
    assert item.sensitivity == DataSensitivity.PUBLIC


# ─── Context feed ────────────────────────────────────────────────
def test_context_feed_blocks_sovereign_for_non_allowlisted_agent() -> None:
    feed = ContextFeedEngine()
    with pytest.raises(PermissionError):
        feed.mint("rogue_agent", "wsp", "x", DataSensitivity.SOVEREIGN, ["read"], {})


def test_context_feed_revoke_and_expiry() -> None:
    feed = ContextFeedEngine()
    pkt = feed.mint("hermes", "wsp", "x", DataSensitivity.PUBLIC, ["read"], {}, ttl_seconds=60)
    assert feed.is_active(pkt.context_id)
    assert feed.revoke(pkt.context_id)
    assert feed.is_active(pkt.context_id) is False


# ─── Memory ──────────────────────────────────────────────────────
def test_memory_redact_for_external() -> None:
    mm = MemoryManager()
    store = mm.store(MemoryKind.SOVEREIGN)
    store.write("sami", "plan", {"x": 1}, DataSensitivity.SOVEREIGN)
    redacted = mm.redact_for_external({
        "ok": True, "sovereign_secret": "x",
        "nested": {"sensitivity": "SOVEREIGN", "v": 1}, "safe": [1, 2],
    })
    assert "sovereign_secret" not in redacted
    assert "nested" not in redacted
    assert redacted["safe"] == [1, 2]
    assert json.dumps(redacted)


# ─── Policy ──────────────────────────────────────────────────────
def test_policy_external_action_triggers_approval_audit_outcome() -> None:
    engine = PolicyEngine()
    outcomes = engine.evaluate({"action_type": "external"})
    assert any(o.policy_id == "external_action_policy_v1" for o in outcomes)
    target = next(o for o in outcomes if o.policy_id == "external_action_policy_v1")
    assert target.requires_approval and target.audit_required and target.outcome_required


# ─── Approvals ───────────────────────────────────────────────────
def _fresh_approval_center() -> tuple[SovereignApprovalCenter, EventBus]:
    bus = EventBus()
    return SovereignApprovalCenter(bus), bus


def test_approval_submit_and_approve() -> None:
    ac, _ = _fresh_approval_center()
    req = ac.submit(
        requested_by="agent", workspace_id="ws1", action_type="proposal",
        sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
        risk_level=RiskLevel.MEDIUM, summary="send proposal",
    )
    approved = ac.approve(req.approval_id, "sami")
    assert approved.decision == ApprovalDecision.APPROVED
    assert approved.approver_id == "sami"


def test_approval_deny_kill_and_pending_filter() -> None:
    ac, _ = _fresh_approval_center()
    r1 = ac.submit(requested_by="a", workspace_id="ws1", action_type="pricing",
                   sovereignty_level=SovereigntyLevel.S3_SAMI_DECISION,
                   risk_level=RiskLevel.HIGH, summary="x")
    r2 = ac.submit(requested_by="b", workspace_id="ws2", action_type="pricing",
                   sovereignty_level=SovereigntyLevel.S3_SAMI_DECISION,
                   risk_level=RiskLevel.HIGH, summary="y")
    ac.deny(r1.approval_id, "sami", "no")
    pending = ac.list_pending(workspace_id="ws2")
    assert len(pending) == 1 and pending[0].approval_id == r2.approval_id
    ac.kill(r2.approval_id)
    assert ac.get(r2.approval_id).decision == ApprovalDecision.KILLED


# ─── Tool gateway ────────────────────────────────────────────────
def _build_gateway() -> tuple[HermesToolGateway, ToolRegistry, ContextFeedEngine]:
    bus = EventBus()
    reg = ToolRegistry()
    log = ToolRuntimeLog()
    ac = SovereignApprovalCenter(bus)
    pe = PolicyEngine()
    return HermesToolGateway(reg, pe, ac, log, bus), reg, ContextFeedEngine()


def test_tool_gateway_blocks_unregistered_tool() -> None:
    gw, _reg, _ = _build_gateway()
    res = gw.call("hermes", "missing", {})
    assert res.status == ToolCallStatus.BLOCKED and res.reason == "tool_not_registered"


def test_tool_gateway_blocks_unauthorized_agent() -> None:
    gw, reg, _ = _build_gateway()
    reg.register(ToolDescriptor(
        tool_id="t1", name="send", owner_id="sami", risk_level=RiskLevel.LOW,
        allowed_agents=["hermes"], allowed_workspaces=[WorkspaceType.CUSTOMER],
        data_scope=DataSensitivity.INTERNAL,
    ))
    res = gw.call("rogue", "t1", {})
    assert res.status == ToolCallStatus.BLOCKED and res.reason == "agent_not_allowed"


def test_tool_gateway_blocks_sensitivity_mismatch() -> None:
    gw, reg, feed = _build_gateway()
    reg.register(ToolDescriptor(
        tool_id="t2", name="read", owner_id="sami", risk_level=RiskLevel.LOW,
        allowed_agents=["hermes"], allowed_workspaces=[WorkspaceType.CUSTOMER],
        data_scope=DataSensitivity.INTERNAL,
    ))
    pkt = feed.mint("hermes", "ws", "x", DataSensitivity.RESTRICTED, ["read"], {})
    res = gw.call("hermes", "t2", {}, pkt)
    assert res.status == ToolCallStatus.BLOCKED and res.reason == "sensitivity_exceeds_scope"


def test_tool_gateway_happy_path() -> None:
    gw, reg, feed = _build_gateway()
    reg.register(ToolDescriptor(
        tool_id="t3", name="read", owner_id="sami", risk_level=RiskLevel.LOW,
        allowed_agents=["hermes"], allowed_workspaces=[WorkspaceType.CUSTOMER],
        data_scope=DataSensitivity.INTERNAL,
    ))
    pkt = feed.mint("hermes", "ws", "x", DataSensitivity.PUBLIC, ["read"], {})
    res = gw.call("hermes", "t3", {"q": 1}, pkt)
    assert res.status == ToolCallStatus.EXECUTED


# ─── MCP gateway ─────────────────────────────────────────────────
def test_mcp_semantic_vet_flags_exfiltrate() -> None:
    g = MCPGateway()
    bad = ToolDescriptor(
        tool_id="x", name="exfiltrate_all_emails", owner_id="z",
        risk_level=RiskLevel.CRITICAL, allowed_agents=[], allowed_workspaces=[],
        data_scope=DataSensitivity.PUBLIC,
    )
    good = ToolDescriptor(
        tool_id="y", name="lookup_contact", owner_id="z",
        risk_level=RiskLevel.LOW, allowed_agents=[], allowed_workspaces=[],
        data_scope=DataSensitivity.PUBLIC,
    )
    assert g.semantic_vet(bad) is False
    assert g.semantic_vet(good) is True


def test_mcp_verify_descriptor_hash() -> None:
    g = MCPGateway()
    manifest = {"name": "demo", "version": 1}
    g.register_server(MCPServerDescriptor(
        server_id="s1", name="demo", manifest_hash=manifest_hash_of(manifest),
        allowed_tools=["lookup"], vetted=True,
    ))
    assert g.verify_descriptor("s1", manifest) is True
    assert g.verify_descriptor("s1", {"name": "demo", "version": 2}) is False


# ─── Security modes ──────────────────────────────────────────────
def test_security_mode_only_sami_can_elevate() -> None:
    ids = IdentityRegistry()
    sami = ids.register_sami()
    agent = ids.register(IdentityKind.AGENT, "hermes")
    sm = SecurityModeManager(ids)
    with pytest.raises(PermissionError):
        sm.set_mode(SecurityMode.LOW_RISK_AUTONOMY, agent.identity_id)
    sm.set_mode(SecurityMode.LOW_RISK_AUTONOMY, sami.identity_id)
    assert sm.current_mode == SecurityMode.LOW_RISK_AUTONOMY


def test_security_mode_can_execute_table() -> None:
    ids = IdentityRegistry(); ids.register_sami()
    sm = SecurityModeManager(ids)
    assert sm.can_execute(RiskLevel.NONE) is True
    assert sm.can_execute(RiskLevel.HIGH) is False


# ─── Incidents ───────────────────────────────────────────────────
def test_incident_high_flips_security_mode_lockdown() -> None:
    ids = IdentityRegistry(); ids.register_sami()
    bus = EventBus()
    sm = SecurityModeManager(ids)
    log = IncidentLog(bus, sm)
    log.create(IncidentType.DATA_EXFILTRATION_ATTEMPT, IncidentSeverity.HIGH,
               "test", "fake leak")
    assert sm.current_mode == SecurityMode.SOVEREIGN_LOCKDOWN
    assert any(e.event_type == "incident.created" for e in bus.tail())


# ─── Events ──────────────────────────────────────────────────────
def test_event_bus_pubsub_and_handler_exception_records_incident() -> None:
    bus = EventBus()
    captured: list[str] = []
    bus.subscribe("ping", lambda e: captured.append(e.event_type))

    incidents: list[tuple[str, str]] = []
    bus.set_incident_sink(lambda k, s: incidents.append((k, s)))
    bus.subscribe("boom", lambda e: (_ for _ in ()).throw(RuntimeError("kaboom")))
    bus.publish(make_event("ping", "t", {}))
    bus.publish(make_event("boom", "t", {}))
    assert captured == ["ping"]
    assert incidents and incidents[0][0] == "agent_behavior_anomaly"


# ─── Agent runtime ───────────────────────────────────────────────
def test_agent_runtime_draft_only_completes_internal_action() -> None:
    ids = IdentityRegistry(); ids.register_sami()
    bus = EventBus()
    feed = ContextFeedEngine()
    pe = PolicyEngine()
    ac = SovereignApprovalCenter(bus)
    sm = SecurityModeManager(ids)
    log = ToolRuntimeLog()
    gw = HermesToolGateway(ToolRegistry(), pe, ac, log, bus)
    rt = AgentRuntime(feed, pe, ac, gw, log, sm, bus)
    run = rt.start("hermes", "ws1", {"action_type": "internal",
                                       "sensitivity": "INTERNAL"})
    assert run.status == RunStatus.COMPLETED


# ─── Money command ───────────────────────────────────────────────
def test_money_expected_revenue_formula() -> None:
    mc = MoneyCommand()
    mc.register_deal(Deal(deal_id="d1", customer="A", stage="proposal",
                          value_sar=100_000, close_probability=0.5,
                          next_step="follow up", last_activity_at="2026-01-01T00:00:00+00:00",
                          owner_id="sami"))
    mc.register_deal(Deal(deal_id="d2", customer="B", stage="negotiation",
                          value_sar=50_000, close_probability=0.8,
                          next_step="send", last_activity_at="2026-01-01T00:00:00+00:00",
                          owner_id="sami"))
    assert mc.expected_revenue() == 90_000.0


# ─── Offers ──────────────────────────────────────────────────────
def test_offer_registry_rejects_missing_fields() -> None:
    reg = OfferRegistry()
    bad = Offer(offer_id="", name="x", buyer="", pain="p", promise="q",
                deliverables=["a"], price_sar=100, metric="m",
                upsell="u", trust_risks=["r"])
    with pytest.raises(OfferGateError):
        reg.register(bad)


def test_offer_state_machine_forbids_skipping() -> None:
    reg = OfferRegistry()
    good = Offer(offer_id="", name="x", buyer="b", pain="p", promise="q",
                 deliverables=["a"], price_sar=100, metric="m",
                 upsell="u", trust_risks=["r"])
    reg.register(good)
    with pytest.raises(OfferGateError):
        reg.transition(good.offer_id, OfferState.SCALED)
    reg.transition(good.offer_id, OfferState.INTERNAL_REVIEW)
    assert reg.get(good.offer_id).state == OfferState.INTERNAL_REVIEW


# ─── Assets ──────────────────────────────────────────────────────
def test_asset_library_reuse_revenue_and_reevaluate() -> None:
    lib = AssetLibrary()
    a = lib.register("template", "Welcome", {}, "sami")
    lib.mark_reused(a.asset_id, 1000.0)
    lib.mark_reused(a.asset_id, 2000.0)
    lib.mark_reused(a.asset_id, 4000.0)
    refreshed = lib.get(a.asset_id)
    assert refreshed.reuse_count == 3
    assert refreshed.revenue_influenced_sar == 7000.0
    assert refreshed.commercializable is True
    # Unused asset is not stale yet (created just now).
    lib.register("template", "Idle", {}, "sami")
    assert lib.reevaluate() == []


# ─── Intelligence graph ─────────────────────────────────────────
def test_intelligence_graph_best_sector() -> None:
    g = IntelligenceGraph()
    g.add_node("fintech", "sector"); g.add_node("d1", "deal")
    g.add_node("retail", "sector"); g.add_node("d2", "deal")
    g.add_edge("fintech", "d1", "produced_revenue", weight=100_000)
    g.add_edge("retail", "d2", "produced_revenue", weight=20_000)
    assert g.best_sector() == "fintech"


# ─── Customer loop ──────────────────────────────────────────────
def test_customer_value_loop_monthly_report_shape() -> None:
    loop = CustomerValueLoop()
    c = loop.onboard("AlphaCo", ["cut_cost_15pct"], "2026-06-01")
    loop.log_activity(c.customer_id, "kickoff")
    loop.log_outcome(c.customer_id, "cost_cut", 30_000)
    r = loop.monthly_value_report(c.customer_id)
    for key in ("activities", "outputs", "outcomes", "estimated_value",
                "risks_reduced", "assets_created", "next_actions", "upsell_recommendation"):
        assert key in r
    assert r["estimated_value"] == 30_000.0


# ─── Partner loop ───────────────────────────────────────────────
def test_partner_trust_check_fails_on_critical_brand_risk() -> None:
    loop = PartnerValueLoop()
    p = loop.scout("PartnerX")
    loop.score(p.partner_id, fit_score=0.8, risks={"brand": RiskLevel.CRITICAL})
    ok, findings = loop.trust_check({"partner_id": p.partner_id, "text": "hi"})
    assert ok is False and "brand_risk_critical" in findings


# ─── Venture loop ───────────────────────────────────────────────
def test_venture_blocks_scale_when_no_outcomes() -> None:
    loop = VentureValueLoop()
    v = loop.create("legal")
    loop.add_signal(v.venture_id, "linkedin", "interested", replied=True)
    loop.define_pain(v.venture_id, {"contract_review": "slow"})
    loop.attach_offer(v.venture_id, "off1")
    loop.add_targets(v.venture_id, 20)
    assert loop.recommend_action(v.venture_id) == "hold:no_outcomes"
    loop.record_pilot(v.venture_id, "AcmeLaw", outcome_recorded=True)
    assert loop.recommend_action(v.venture_id) == "scale"


# ─── Readiness ──────────────────────────────────────────────────
def test_public_api_readiness_flags_missing() -> None:
    r = PublicAPIReadiness()
    ready, missing = r.assess()
    assert ready is False and "metering" in missing


def test_marketplace_readiness_flags_missing() -> None:
    r = MarketplaceReadiness()
    ready, missing = r.assess()
    assert ready is False and "vendor_vetting" in missing


# ─── Packaging ──────────────────────────────────────────────────
def test_packaging_recommend_tier() -> None:
    assert recommend_offer_tier({"annual_revenue_sar": 1_000_000, "employees": 10}) == "Entry"
    assert recommend_offer_tier({"annual_revenue_sar": 10_000_000, "employees": 100}) == "Expansion"
    assert recommend_offer_tier({"annual_revenue_sar": 100_000_000, "employees": 500}) == "Enterprise"
    assert recommend_offer_tier({"sector": "bank", "annual_revenue_sar": 100_000}) == "Enterprise"


# ─── Facade ─────────────────────────────────────────────────────
def test_sovereign_control_plane_submit_signal_happy_path() -> None:
    cp = get_control_plane()
    before = len(cp.events_tail(10_000))
    plan = cp.submit_signal({
        "opportunity_id": "opp-test", "workspace_kind": "CUSTOMER",
        "action_type": "internal", "payload": {"q": "what is value?"},
    })
    assert plan.opportunity_id == "opp-test"
    assert plan.selected_engine
    assert any(e.event_type == "hermes.routed" for e in cp.events_tail(10_000)[before:])
    assert json.dumps(plan.to_dict())


def test_sovereign_control_plane_health_round_trip_json() -> None:
    cp = get_control_plane()
    snap = cp.health()
    json.dumps(snap)
    assert "security_mode" in snap


# ─── Extra coverage — money, mcp, partner, observability, ... ──
def test_money_command_full_surface() -> None:
    mc = MoneyCommand()
    mc.register_deal(Deal(deal_id="d1", customer="A", stage="proposal",
                          value_sar=100_000, close_probability=0.5,
                          next_step="follow", last_activity_at="2024-01-01T00:00:00+00:00",
                          owner_id="sami", upsell_ready=True, partner_id="p1",
                          paid=True, payment_due_at="2026-06-01"))
    mc.register_deal(Deal(deal_id="d2", customer="B", stage="negotiation",
                          value_sar=50_000, close_probability=0.8,
                          next_step="send", last_activity_at="2020-01-01T00:00:00+00:00",
                          owner_id="sami", blockers=["legal"],
                          payment_due_at="2026-07-01"))
    assert mc.cash_now() == 100_000.0
    assert mc.pipeline() == 50_000.0
    assert len(mc.open_proposals()) == 1
    assert len(mc.stuck_deals(threshold_days=14)) == 1
    assert len(mc.pending_payments()) == 1
    assert len(mc.upsells()) == 1
    assert mc.partner_revenue() == {"p1": 100_000.0}
    best = mc.best_next_action()
    assert best is not None and best["deal_id"] == "d2"
    snap = mc.snapshot()
    json.dumps(snap)


def test_mcp_gateway_runtime_and_kill() -> None:
    g = MCPGateway()
    manifest = {"name": "demo", "version": 1}
    g.register_server(MCPServerDescriptor(
        server_id="s1", name="demo", manifest_hash=manifest_hash_of(manifest),
        allowed_tools=["lookup"], vetted=True,
    ))
    ok = g.call("s1", "lookup", {"a": 1})
    assert ok["ok"] is True
    bad = g.call("s1", "missing", {})
    assert bad["ok"] is False and bad["reason"] == "tool_not_allowed"
    huge = g.call("s1", "lookup", {"a": "x" * 60_000})
    assert huge["ok"] is False
    assert g.kill("s1") is True
    after = g.call("s1", "lookup", {})
    assert after["ok"] is False and after["reason"] == "kill_switch_enabled"
    risk_low = g.runtime_anomaly_check({"args": "abc"})
    assert risk_low.value == "low"


def test_partner_loop_full_flow() -> None:
    loop = PartnerValueLoop()
    p = loop.scout("PX")
    loop.score(p.partner_id, fit_score=0.9, risks={"brand": RiskLevel.LOW})
    loop.agree(p.partner_id, revenue_share_pct=20.0)
    loop.onboard(p.partner_id)
    loop.log_revenue(p.partner_id, 120_000, deal_id="d1")
    review = loop.performance_review(p.partner_id)
    assert review["total_revenue_sar"] == 120_000.0
    assert loop.recommend_action(p.partner_id) == "scale"
    # Unknown partner check.
    ok, findings = loop.trust_check({"partner_id": "missing", "text": ""})
    assert ok is False and "unknown_partner" in findings


def test_observability_red_flags_and_dashboard() -> None:
    cp = get_control_plane()
    flags = cp.red_flags.scan()
    assert isinstance(flags, list)
    # Dashboard methods all return dicts.
    for fn in (cp.dashboard.agent_performance, cp.dashboard.tool_risk,
               cp.dashboard.approval_queue, cp.dashboard.outcome_graph,
               cp.dashboard.cost_dashboard, cp.dashboard.incident_dashboard,
               cp.dashboard.asset_creation):
        assert isinstance(fn(), dict)


def test_intelligence_graph_aggregates() -> None:
    g = IntelligenceGraph()
    g.add_node("msg1", "message"); g.add_node("d1", "deal")
    g.add_edge("msg1", "d1", "won_reply", weight=3)
    g.add_node("off1", "offer"); g.add_edge("off1", "d1", "closed_deal", weight=2)
    g.add_node("par1", "partner"); g.add_edge("par1", "d1", "delivered_revenue", weight=5)
    g.add_node("ag1", "agent"); g.add_edge("ag1", "d1", "produced_revenue", weight=1)
    g.add_node("t_bad", "tool", {"risk": "high"})
    g.add_node("obj1", "objection")
    g.add_edge("obj1", "d1", "raised_in_deal")
    g.add_edge("obj1", "d2", "raised_in_deal")
    g.add_node("pp1", "price_point", {"accepted": True, "price_sar": 49_000})
    assert g.best_message() == "msg1"
    assert g.most_profitable_offer() == "off1"
    assert g.best_partner() == "par1"
    assert "ag1" in g.revenue_producing_agents()
    assert "t_bad" in g.risky_tools()
    assert "obj1" in g.recurring_objections()
    assert g.accepted_prices() == [49_000.0]


def test_agent_runtime_blocks_when_context_refused() -> None:
    ids = IdentityRegistry(); ids.register_sami()
    bus = EventBus(); feed = ContextFeedEngine(); pe = PolicyEngine()
    ac = SovereignApprovalCenter(bus); sm = SecurityModeManager(ids)
    log = ToolRuntimeLog()
    gw = HermesToolGateway(ToolRegistry(), pe, ac, log, bus)
    rt = AgentRuntime(feed, pe, ac, gw, log, sm, bus)
    run = rt.start("rogue_agent", "ws1",
                   {"sensitivity": "SOVEREIGN", "action_type": "internal"})
    assert run.status == RunStatus.BLOCKED


def test_customer_loop_upsell_tiers() -> None:
    loop = CustomerValueLoop()
    c = loop.onboard("Big", ["scale"], "2026-12-01")
    loop.log_outcome(c.customer_id, "saved", 150_000)
    loop.log_output(c.customer_id, "report.pdf")
    loop.log_asset(c.customer_id, "ast_x")
    loop.log_risk_reduced(c.customer_id, "vendor_lock_in")
    r = loop.monthly_value_report(c.customer_id)
    assert r["upsell_recommendation"] == "expansion_tier"
    c2 = loop.onboard("Mid", ["scale"], "2026-12-01")
    loop.log_outcome(c2.customer_id, "saved", 30_000)
    assert loop.monthly_value_report(c2.customer_id)["upsell_recommendation"] == "addon_module"


def test_incidents_list_and_resolve() -> None:
    ids = IdentityRegistry(); ids.register_sami()
    bus = EventBus(); sm = SecurityModeManager(ids)
    log = IncidentLog(bus, sm)
    inc = log.create(IncidentType.TOOL_ABUSE, IncidentSeverity.LOW,
                     "test", "minor abuse")
    assert log.get(inc.incident_id) is inc
    listed = log.list(severity=IncidentSeverity.LOW)
    assert inc in listed
    resolved = log.resolve(inc.incident_id, "investigated")
    assert resolved.resolution_notes == "investigated"


def test_policy_engine_disable_and_register() -> None:
    engine = PolicyEngine()
    engine.disable("api_policy_v1")
    out = engine.evaluate({"workspace_kind": "API"})
    assert not any(o.policy_id == "api_policy_v1" for o in out)


def test_memory_query_and_forget() -> None:
    mm = MemoryManager()
    store = mm.store(MemoryKind.OUTCOME)
    store.write("c1", "k1", 1, DataSensitivity.PUBLIC)
    store.write("c1", "k2", 2, DataSensitivity.PUBLIC)
    items = store.query("c1", lambda e: e.key == "k2")
    assert len(items) == 1 and items[0].value == 2
    assert store.forget("c1", "k1") is True
    assert store.read("c1", "k1") is None


def test_ui_philosophy_constants_present() -> None:
    from dealix.sovereign_control_plane import ui_philosophy
    assert len(ui_philosophy.UI_PAGE_QUESTIONS) == 5
    assert len(ui_philosophy.UI_SECTIONS) == 6


def test_identity_sami_idempotent_and_kind_listing() -> None:
    reg = IdentityRegistry()
    a = reg.register_sami(); b = reg.register_sami()
    assert a.identity_id == b.identity_id
    reg.register(IdentityKind.AGENT, "h1")
    reg.register(IdentityKind.AGENT, "h2")
    assert len(reg.list_by_kind(IdentityKind.AGENT)) == 2
    with pytest.raises(ValueError):
        reg.register(IdentityKind.SAMI, "another")


def test_classification_explicit_hint() -> None:
    c = Classifier()
    item = c.classify("anything", hints={"sensitivity": "CONFIDENTIAL", "item_id": "x"})
    assert item.sensitivity == DataSensitivity.CONFIDENTIAL and item.item_id == "x"

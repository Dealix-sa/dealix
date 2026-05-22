"""Tests for the Dealix Agent Organization — org chart, daily cycle, API.

Doctrine under test: governed autonomy. The org runs work automatically,
but every externally-visible output is draft-only and approval-gated —
no agent can auto-complete its own external work.
"""

from __future__ import annotations

import pytest
from httpx import AsyncClient

from auto_client_acquisition.agent_org.approval_routing import (
    route_items_to_approvals,
    route_report_to_approvals,
)
from auto_client_acquisition.agent_org.cycle_store import (
    CycleStore,
    get_default_cycle_store,
    reset_default_cycle_store,
)
from auto_client_acquisition.agent_org.org_chart import (
    TIER_CHIEF,
    TIER_DIRECTOR,
    TIER_OPERATOR,
    all_roles,
    chief,
    directors,
    external_roles,
    get_role,
    operators,
    operators_under,
    org_chart_dict,
    validate_org,
)
from auto_client_acquisition.agent_org.orchestrator import (
    STATUS_INTERNAL,
    STATUS_PENDING_APPROVAL,
    run_daily_cycle,
)
from auto_client_acquisition.agent_os.autonomy_levels import AutonomyLevel
from auto_client_acquisition.approval_center import ApprovalStore


@pytest.fixture(autouse=True)
def _fresh_cycle_store() -> None:
    """Wipe the process-wide cycle store before every test in this file."""
    reset_default_cycle_store()


# ── Org chart structure ──────────────────────────────────────────────


def test_org_has_expected_pyramid_shape() -> None:
    assert len(all_roles()) == 25
    assert len(directors()) == 6
    assert len(operators()) == 18
    assert chief().id == "chief_of_staff"


def test_validate_org_is_healthy() -> None:
    assert validate_org() == []


def test_every_director_reports_to_chief() -> None:
    for d in directors():
        assert d.tier == TIER_DIRECTOR
        assert d.reports_to == "chief_of_staff"


def test_every_operator_reports_to_a_director() -> None:
    director_ids = {d.id for d in directors()}
    for op in operators():
        assert op.tier == TIER_OPERATOR
        assert op.reports_to in director_ids


def test_each_director_has_operators() -> None:
    for d in directors():
        assert len(operators_under(d.id)) == 3


def test_chief_reports_to_no_one() -> None:
    assert chief().tier == TIER_CHIEF
    assert chief().reports_to is None


def test_get_role_round_trips_and_unknown_raises() -> None:
    assert get_role("revenue_director").name_en == "Revenue Director"
    with pytest.raises(KeyError):
        get_role("no_such_agent")


def test_org_chart_dict_is_serializable_tree() -> None:
    chart = org_chart_dict()
    assert chart["headcount"] == 25
    assert chart["tiers"] == {"chief": 1, "directors": 6, "operators": 18}
    assert len(chart["chief"]["directs"]) == 6
    for d in chart["chief"]["directs"]:
        assert len(d["directs"]) == 3


# ── Doctrine: autonomy ceiling on external output ────────────────────


def test_external_output_never_exceeds_draft_autonomy() -> None:
    """The core non-negotiable: nothing externally visible runs above L2."""
    for role in external_roles():
        assert role.autonomy <= AutonomyLevel.L2_DRAFT, role.id


def test_no_role_exceeds_recommend_autonomy() -> None:
    """L4/L5 (auto-execute) is reserved — no org role may claim it."""
    for role in all_roles():
        assert role.autonomy <= AutonomyLevel.L3_RECOMMEND, role.id


# ── Daily executive cycle ────────────────────────────────────────────


def test_daily_cycle_runs_whole_org() -> None:
    report = run_daily_cycle()
    assert report.agents_run == 25
    assert report.cycle_id.startswith("cycle")
    assert report.work_items


def test_cycle_counts_are_internally_consistent() -> None:
    report = run_daily_cycle()
    assert report.items_total == len(report.work_items)
    assert report.items_pending_approval + report.items_internal == report.items_total


def test_every_external_work_item_is_pending_approval() -> None:
    """No agent can mark its own external output as done — doctrine."""
    report = run_daily_cycle()
    external = [w for w in report.work_items if w.external]
    assert external, "expected some external drafts"
    for item in external:
        assert item.status == STATUS_PENDING_APPROVAL, item.agent_id


def test_internal_items_are_marked_internal_done() -> None:
    report = run_daily_cycle()
    for item in report.work_items:
        if not item.external:
            assert item.status == STATUS_INTERNAL, item.agent_id


def test_cycle_produces_bilingual_founder_brief() -> None:
    report = run_daily_cycle(run_date="2026-05-18")
    assert "2026-05-18" in report.founder_brief_en
    assert "2026-05-18" in report.founder_brief_ar
    # Arabic brief actually contains Arabic script.
    assert any("؀" <= ch <= "ۿ" for ch in report.founder_brief_ar)


def test_cycle_is_deterministic_for_same_context() -> None:
    a = run_daily_cycle(run_date="2026-05-18", context={"outreach_due": 5})
    b = run_daily_cycle(run_date="2026-05-18", context={"outreach_due": 5})
    assert a.items_total == b.items_total
    assert a.items_pending_approval == b.items_pending_approval


def test_context_drives_operator_output() -> None:
    report = run_daily_cycle(context={"outreach_due": 11})
    outreach = [w for w in report.work_items if w.agent_id == "outreach_drafter"]
    assert outreach and outreach[0].payload["count"] == 11


def test_high_approval_load_raises_escalation() -> None:
    report = run_daily_cycle(context={"outreach_due": 99})
    assert any("approval-load" in e for e in report.escalations)


def test_chief_brief_is_the_final_work_item() -> None:
    report = run_daily_cycle()
    last = report.work_items[-1]
    assert last.agent_id == "chief_of_staff"
    assert last.kind == "founder_brief"
    assert last.external is False


# ── API surface ──────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_api_status(async_client: AsyncClient) -> None:
    resp = await async_client.get("/api/v1/agent-org/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["headcount"] == 25
    assert body["guardrails"]["no_auto_send"] is True


@pytest.mark.asyncio
async def test_api_chart(async_client: AsyncClient) -> None:
    resp = await async_client.get("/api/v1/agent-org/chart")
    assert resp.status_code == 200
    assert resp.json()["headcount"] == 25


@pytest.mark.asyncio
async def test_api_agents_list(async_client: AsyncClient) -> None:
    resp = await async_client.get("/api/v1/agent-org/agents")
    assert resp.status_code == 200
    assert resp.json()["count"] == 25


@pytest.mark.asyncio
async def test_api_agent_detail_and_404(async_client: AsyncClient) -> None:
    ok = await async_client.get("/api/v1/agent-org/agents/chief_of_staff")
    assert ok.status_code == 200
    assert ok.json()["name_en"] == "Chief of Staff"

    missing = await async_client.get("/api/v1/agent-org/agents/ghost")
    assert missing.status_code == 404


@pytest.mark.asyncio
async def test_api_validate(async_client: AsyncClient) -> None:
    resp = await async_client.get("/api/v1/agent-org/validate")
    assert resp.status_code == 200
    body = resp.json()
    assert body["healthy"] is True
    assert body["problems"] == []


@pytest.mark.asyncio
async def test_api_daily_cycle_run(async_client: AsyncClient) -> None:
    resp = await async_client.post(
        "/api/v1/agent-org/daily-cycle/run",
        json={"run_date": "2026-05-18", "context": {"outreach_due": 7}},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["agents_run"] == 25
    assert body["run_date"] == "2026-05-18"
    external = [w for w in body["work_items"] if w["external"]]
    assert external
    assert all(w["status"] == "pending_approval" for w in external)


@pytest.mark.asyncio
async def test_api_daily_cycle_rejects_bad_context(async_client: AsyncClient) -> None:
    resp = await async_client.post(
        "/api/v1/agent-org/daily-cycle/run",
        json={"context": "not-an-object"},
    )
    assert resp.status_code == 422


# ── Approval routing ─────────────────────────────────────────────────


def test_route_report_pushes_every_external_draft() -> None:
    store = ApprovalStore()
    report = run_daily_cycle()
    expected = sum(1 for w in report.work_items if w.external)
    routed = route_report_to_approvals(report, store=store)
    assert len(routed) == expected
    assert len(store.list_pending()) == expected


def test_route_report_skips_internal_items() -> None:
    store = ApprovalStore()
    report = run_daily_cycle()
    internal_ids = {w.id for w in report.work_items if not w.external}
    routed = route_report_to_approvals(report, store=store)
    routed_object_ids = {r.object_id for r in routed}
    assert routed_object_ids.isdisjoint(internal_ids)


def test_routed_requests_are_draft_only_doctrine() -> None:
    """The non-negotiable: nothing routed by the org may be approved-to-send."""
    store = ApprovalStore()
    report = run_daily_cycle()
    routed = route_report_to_approvals(report, store=store)
    assert routed
    assert all(r.action_mode == "draft_only" for r in routed)
    assert all(r.object_type == "agent_org_work_item" for r in routed)


def test_routed_requests_have_bilingual_summaries() -> None:
    store = ApprovalStore()
    report = run_daily_cycle()
    routed = route_report_to_approvals(report, store=store)
    for r in routed:
        assert r.summary_ar and r.summary_en


def test_route_items_helper_accepts_iterable() -> None:
    store = ApprovalStore()
    report = run_daily_cycle()
    external = [w for w in report.work_items if w.external]
    routed = route_items_to_approvals(external, store=store)
    assert len(routed) == len(external)


# ── Cycle store ──────────────────────────────────────────────────────


def test_cycle_store_round_trip() -> None:
    store = CycleStore()
    report = run_daily_cycle()
    store.add(report)
    assert len(store) == 1
    assert store.get(report.cycle_id) is report
    assert store.latest() is report
    assert store.list_recent() == [report]


def test_cycle_store_evicts_oldest_when_capped() -> None:
    store = CycleStore(max_cycles=3)
    reports = [run_daily_cycle() for _ in range(5)]
    for r in reports:
        store.add(r)
    assert len(store) == 3
    # The two oldest are gone; the three newest remain.
    kept = {r.cycle_id for r in store.list_recent(limit=10)}
    assert kept == {reports[-1].cycle_id, reports[-2].cycle_id, reports[-3].cycle_id}


def test_cycle_store_list_recent_is_newest_first() -> None:
    store = CycleStore()
    a = run_daily_cycle()
    b = run_daily_cycle()
    store.add(a)
    store.add(b)
    recent = store.list_recent()
    assert recent[0] is b
    assert recent[1] is a


def test_default_cycle_store_is_singleton() -> None:
    assert get_default_cycle_store() is get_default_cycle_store()


# ── API: persistence + routing + history ─────────────────────────────


@pytest.mark.asyncio
async def test_api_daily_cycle_persists_and_routes(
    async_client: AsyncClient,
) -> None:
    resp = await async_client.post("/api/v1/agent-org/daily-cycle/run", json={})
    assert resp.status_code == 200
    body = resp.json()
    assert body["persisted"] is True
    assert body["routed_to_approvals"] == body["items_pending_approval"]
    assert len(get_default_cycle_store()) == 1


@pytest.mark.asyncio
async def test_api_daily_cycle_no_route_when_disabled(
    async_client: AsyncClient,
) -> None:
    resp = await async_client.post(
        "/api/v1/agent-org/daily-cycle/run",
        json={"route_to_approvals": False, "persist": False},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["routed_to_approvals"] == 0
    assert body["persisted"] is False
    assert len(get_default_cycle_store()) == 0


@pytest.mark.asyncio
async def test_api_cycles_list_and_detail(async_client: AsyncClient) -> None:
    run_a = await async_client.post("/api/v1/agent-org/daily-cycle/run", json={})
    run_b = await async_client.post("/api/v1/agent-org/daily-cycle/run", json={})
    a_id = run_a.json()["cycle_id"]
    b_id = run_b.json()["cycle_id"]

    listing = await async_client.get("/api/v1/agent-org/cycles?limit=10")
    assert listing.status_code == 200
    body = listing.json()
    assert body["count"] == 2
    ids = [c["cycle_id"] for c in body["cycles"]]
    assert ids == [b_id, a_id]  # newest first

    detail = await async_client.get(f"/api/v1/agent-org/cycles/{a_id}")
    assert detail.status_code == 200
    assert detail.json()["cycle_id"] == a_id


@pytest.mark.asyncio
async def test_api_cycles_latest_404_when_empty(async_client: AsyncClient) -> None:
    resp = await async_client.get("/api/v1/agent-org/cycles/latest")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_api_cycles_detail_unknown_id_404(async_client: AsyncClient) -> None:
    resp = await async_client.get("/api/v1/agent-org/cycles/cycle_ghost")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_api_cycles_list_rejects_bad_limit(async_client: AsyncClient) -> None:
    too_big = await async_client.get("/api/v1/agent-org/cycles?limit=999")
    assert too_big.status_code == 422
    too_small = await async_client.get("/api/v1/agent-org/cycles?limit=0")
    assert too_small.status_code == 422

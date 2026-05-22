"""Full-Ops operating loop — WS5 behavioural tests.

Covers: ``run_tick`` senses WorkItems, assigns them to roster agents,
external actions create approval requests, ZERO sends/charges occur, and
every agent autonomy level is L1–L4 (no L5 anywhere).
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.agent_os import (
    AutonomyLevel,
    clear_for_test,
    list_agents,
)
from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.full_ops.agent_roster import (
    ROSTER,
    build_roster_cards,
    capability_map,
    pyramid_status,
    register_full_ops_agents,
)
from auto_client_acquisition.full_ops.operating_loop import (
    assign,
    execute,
    gate,
    read_tick_ledger,
    record,
    run_tick,
    sense,
)
from auto_client_acquisition.full_ops.work_item import WorkItem
from auto_client_acquisition.full_ops.work_queue import WorkQueue


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    """Fresh registry, store, queue and ledger per test."""
    monkeypatch.setenv("DEALIX_AGENT_REGISTRY_PATH", str(tmp_path / "agents.jsonl"))
    monkeypatch.setenv(
        "DEALIX_FULL_OPS_LEDGER_PATH", str(tmp_path / "ticks.jsonl")
    )
    clear_for_test()
    get_default_approval_store().clear()
    yield
    clear_for_test()
    get_default_approval_store().clear()


def _internal_item() -> WorkItem:
    return WorkItem.make(
        os_type="delivery",
        title_ar="خطوة تسليم داخلية",
        title_en="Internal delivery step",
        source="test",
        priority="p2",
        action_mode="draft_only",
    )


def _external_item() -> WorkItem:
    return WorkItem.make(
        os_type="sales",
        title_ar="مسودة متابعة مع العميل",
        title_en="Customer follow-up draft",
        source="test",
        priority="p1",
        action_mode="approval_required",
        customer_id="cust_001",
    )


# ── Roster (WS2) ───────────────────────────────────────────────────


def test_register_full_ops_agents_is_idempotent() -> None:
    first = register_full_ops_agents()
    second = register_full_ops_agents()
    assert len(first) == len(ROSTER)
    assert len(second) == len(ROSTER)
    assert {c.agent_id for c in first} == {c.agent_id for c in second}


def test_roster_has_three_tiers() -> None:
    tiers = {entry.tier for entry in ROSTER}
    assert tiers == {1, 2, 3}


def test_no_agent_uses_l5() -> None:
    for card in build_roster_cards():
        assert card.autonomy_level <= int(AutonomyLevel.L4_AUTO_WITH_AUDIT)
        assert card.autonomy_level < int(AutonomyLevel.L5_FULLY_AUTONOMOUS)


def test_registered_agents_respect_l1_to_l4() -> None:
    register_full_ops_agents()
    for card in list_agents():
        assert 1 <= card.autonomy_level <= 4


def test_capability_map_covers_every_os() -> None:
    cmap = capability_map()
    for os_type in (
        "growth",
        "sales",
        "support",
        "customer_success",
        "delivery",
        "executive",
        "compliance",
    ):
        assert os_type in cmap


def test_pyramid_status_flags_l5_forbidden() -> None:
    register_full_ops_agents()
    status = pyramid_status()
    assert status["l5_forbidden"] is True
    assert status["max_autonomy_level"] == 4
    assert status["total_agents"] == len(ROSTER)


# ── Loop steps (WS1) ───────────────────────────────────────────────


def test_sense_collects_seeded_items() -> None:
    q = WorkQueue()
    sensed = sense(queue=q, seed_items=[_internal_item(), _external_item()])
    assert len(sensed) == 2


def test_assign_routes_every_item_to_an_agent() -> None:
    items = [_internal_item(), _external_item()]
    assignments = assign(items)
    assert len(assignments) == 2
    valid_ids = {entry.agent_id for entry in ROSTER}
    for record_ in assignments:
        assert record_["agent_id"] in valid_ids


def test_execute_produces_internal_only_drafts() -> None:
    drafts = execute(assign([_external_item()]))
    assert len(drafts) == 1
    assert drafts[0]["artifact"]["internal_only"] is True
    assert drafts[0]["artifact"]["kind"] == "draft"


def test_gate_creates_approval_for_external_action() -> None:
    gated = gate(execute(assign([_external_item()])))
    assert gated[0]["gate"] == "approval_required"
    assert gated[0]["approval"] is not None
    assert get_default_approval_store().list_pending()


def test_gate_passes_through_internal_only_item() -> None:
    gated = gate(execute(assign([_internal_item()])))
    assert gated[0]["gate"] == "internal_only"
    assert gated[0]["approval"] is None


def test_record_appends_to_ledger() -> None:
    record({"tick_id": "t1", "work_items_sensed": 0})
    record({"tick_id": "t2", "work_items_sensed": 1})
    rows = read_tick_ledger()
    assert len(rows) == 2
    assert rows[0]["tick_id"] == "t2"  # newest first


# ── run_tick end-to-end ────────────────────────────────────────────


def test_run_tick_returns_structured_summary() -> None:
    q = WorkQueue()
    q.add_many([_internal_item(), _external_item()])
    summary = run_tick(queue=q)
    assert summary["work_items_sensed"] == 2
    assert len(summary["assignments"]) == 2
    assert summary["drafts_produced"] == 2
    assert summary["tick_id"].startswith("tick_")


def test_run_tick_performs_zero_sends_and_charges() -> None:
    q = WorkQueue()
    q.add_many([_external_item(), _internal_item()])
    summary = run_tick(queue=q)
    assert summary["sends"] == 0
    assert summary["charges"] == 0
    assert summary["internal_only"] is True


def test_run_tick_queues_external_action_as_approval() -> None:
    q = WorkQueue()
    q.add(_external_item())
    summary = run_tick(queue=q)
    assert summary["approvals_created"] == 1
    assert len(summary["approvals_required"]) == 1
    assert summary["approvals_required"][0]["action_mode"] == "approval_required"


def test_run_tick_records_to_ledger() -> None:
    q = WorkQueue()
    q.add(_internal_item())
    summary = run_tick(queue=q)
    assert "ledger_path" in summary
    assert read_tick_ledger()


def test_run_tick_with_seed_items() -> None:
    q = WorkQueue()
    summary = run_tick(queue=q, seed_items=[_external_item()])
    assert summary["work_items_sensed"] == 1


def test_run_tick_hard_gates_present() -> None:
    summary = run_tick(queue=WorkQueue())
    gates = summary["hard_gates"]
    assert gates["no_live_send"] is True
    assert gates["no_live_charge"] is True
    assert gates["l5_forbidden"] is True
    assert gates["max_autonomy_level"] == 4


def test_run_tick_is_idempotent_for_queued_external_items() -> None:
    """Repeated ticks against the same queued WorkItem must NOT pile up
    duplicate pending approvals. See PR #311 Codex review (P1).
    """
    q = WorkQueue()
    q.add(_external_item())

    first = run_tick(queue=q)
    second = run_tick(queue=q)

    assert first["work_items_sensed"] == 1
    assert second["work_items_sensed"] == 1
    # First tick creates exactly one approval; the second skips it.
    assert len(first["approvals_required"]) == 1
    assert first["dedup_skipped_count"] == 0
    assert len(second["approvals_required"]) == 0
    assert second["dedup_skipped_count"] == 1
    # Approval store ends with one pending request, not two.
    pending = get_default_approval_store().list_pending()
    assert len(pending) == 1

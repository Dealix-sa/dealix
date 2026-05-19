"""Tests for the governed day entrypoint (M3) and governance log (M4)."""
from __future__ import annotations

import pytest

from auto_client_acquisition.governance_os import governance_log
from auto_client_acquisition.orchestrator.governed_day import (
    GovernedDayResult,
    run_governed_day,
)
from auto_client_acquisition.revenue_memory.event_store import InMemoryEventStore


@pytest.fixture(autouse=True)
def _isolated_governance_store():
    """Each test gets a fresh in-memory governance event store."""
    governance_log.set_governance_store(InMemoryEventStore())
    yield
    governance_log.set_governance_store(None)


# ─── Governance log (M4) ─────────────────────────────────────────


def test_record_and_query_blocked() -> None:
    governance_log.record_blocked(action_type="draft_email", reason="cold outreach gate")
    governance_log.record_approval_created(approval_id="apr_1", action_type="draft_email")
    blocked = governance_log.query_blocked()
    assert len(blocked) == 1
    assert blocked[0]["event_type"] == "governance.action_blocked"
    assert blocked[0]["payload"]["reason"] == "cold outreach gate"


def test_record_approval_decision_queryable() -> None:
    governance_log.record_approval_decision(
        approval_id="apr_9", decision="approved", who="founder"
    )
    recent = governance_log.query_recent()
    assert any(e["event_type"] == "governance.approval_decision" for e in recent)


def test_phase_events_recorded() -> None:
    governance_log.record_phase(phase="p1", status="started")
    governance_log.record_phase(phase="p1", status="ok", summary="done")
    recent = governance_log.query_recent()
    types = {e["event_type"] for e in recent}
    assert "governance.phase_started" in types
    assert "governance.phase_completed" in types


# ─── Governed day (M3) ───────────────────────────────────────────


def test_run_governed_day_default_phases_ok() -> None:
    result = run_governed_day()
    assert isinstance(result, GovernedDayResult)
    assert result.verdict == "ok"
    assert result.counts["phases"] == 3
    assert result.counts["ok"] == 3
    # every phase emitted started + completed events
    recent = governance_log.query_recent(limit=50)
    assert sum(1 for e in recent if e["event_type"] == "governance.phase_started") == 3


def test_run_governed_day_degraded_phase_does_not_crash() -> None:
    def _boom() -> dict:
        raise RuntimeError("phase exploded")

    result = run_governed_day(phases=[("ok_phase", lambda: {"summary": "fine"}),
                                      ("bad_phase", _boom)])
    assert result.verdict == "degraded"
    bad = next(p for p in result.phases if p.name == "bad_phase")
    assert bad.status == "degraded"
    assert "phase exploded" in bad.error
    # the failure was recorded, not raised
    recent = governance_log.query_recent()
    assert any(e["event_type"] == "governance.phase_degraded" for e in recent)


def test_dry_run_records_phases_without_executing() -> None:
    executed = []
    result = run_governed_day(
        phases=[("watched", lambda: executed.append(1) or {})], dry_run=True
    )
    assert executed == []  # phase fn was never called
    assert result.phases[0].summary == "dry-run: not executed"
    assert result.verdict == "ok"


def test_to_dict_is_json_safe() -> None:
    result = run_governed_day(dry_run=True, phases=[("p", lambda: {})])
    d = result.to_dict()
    assert d["verdict"] == "ok"
    assert d["phases"][0]["name"] == "p"

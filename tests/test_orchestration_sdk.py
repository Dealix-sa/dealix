"""Tests for the agent orchestration SDK (M5) — the unified governed surface."""
from __future__ import annotations

import pytest

from auto_client_acquisition.approval_center.approval_store import (
    reset_default_approval_store,
)
from auto_client_acquisition.governance_os import governance_log
from auto_client_acquisition.orchestrator import orchestration_sdk as sdk
from auto_client_acquisition.revenue_memory.event_store import InMemoryEventStore


@pytest.fixture(autouse=True)
def _isolated():
    reset_default_approval_store()
    governance_log.set_governance_store(InMemoryEventStore())
    yield
    reset_default_approval_store()
    governance_log.set_governance_store(None)


def test_queue_draft_then_visible_in_pending() -> None:
    appr = sdk.queue_draft(
        action_type="draft_email",
        object_type="outreach",
        object_id="msg_1",
        channel="email",
        lead_id="lead_1",
    )
    assert appr.approval_id in {a.approval_id for a in sdk.pending_approvals()}


def test_advance_lead_forward_only() -> None:
    ok = sdk.advance_lead(
        lead_id="lead_1", current=sdk.Stage.CAPTURED, target=sdk.Stage.QUALIFIED
    )
    assert ok.allowed
    bad = sdk.advance_lead(
        lead_id="lead_1", current=sdk.Stage.PAID, target=sdk.Stage.CAPTURED
    )
    assert not bad.allowed


def test_lead_next_stages() -> None:
    nxt = sdk.lead_next_stages(sdk.Stage.CAPTURED)
    assert sdk.Stage.QUALIFIED in nxt
    assert sdk.Stage.LOST in nxt


def test_plan_follow_ups_returns_cadence() -> None:
    plan = sdk.plan_follow_ups(channel="email", touches=4)
    assert len(plan) == 4
    assert all(t.channel == "email" for t in plan)


def test_log_blocked_is_queryable() -> None:
    sdk.log_blocked(action_type="cold_whatsapp", reason="non-negotiable: no cold WhatsApp")
    events = sdk.governance_events()
    assert any(e["event_type"] == "governance.action_blocked" for e in events)


def test_run_day_returns_result() -> None:
    result = sdk.run_day(dry_run=True)
    assert result.verdict in ("ok", "degraded", "blocked")

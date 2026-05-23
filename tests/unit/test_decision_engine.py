"""Decision engine produces the expected next actions."""
from __future__ import annotations

from datetime import datetime, timezone

from control_plane.company_state import snapshot
from control_plane.decision_engine import DecisionEngine


def _state(**kw):
    base = dict(
        as_of=datetime(2026, 5, 23, tzinfo=timezone.utc),
        leads_this_week=0,
        proposals_out=0,
        pending_approvals=0,
        runway_months=12.0,
        company_health_score=80,
    )
    base.update(kw)
    return snapshot(**base)


def test_recommends_clearing_approvals_when_pending():
    decisions = DecisionEngine().propose(_state(pending_approvals=3))
    assert any("Clear" in d.label for d in decisions)


def test_flags_runway_below_threshold():
    decisions = DecisionEngine().propose(_state(runway_months=2.0))
    assert any(d.approval_class == "founder_capital" for d in decisions)


def test_recommends_lead_top_up_when_below_target():
    decisions = DecisionEngine().propose(_state(leads_this_week=5))
    assert any("Add" in d.label and "leads" in d.label for d in decisions)


def test_returns_fallback_when_everything_is_clean():
    decisions = DecisionEngine().propose(_state(
        leads_this_week=25, proposals_out=1, runway_months=12.0,
    ))
    assert decisions
    assert any("review" in d.label.lower() for d in decisions)

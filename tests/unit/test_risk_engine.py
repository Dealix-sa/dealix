"""RiskEngine flags the expected severities."""
from __future__ import annotations

from datetime import datetime, timezone

from control_plane.company_state import snapshot
from control_plane.risk_engine import RiskEngine


def _state(**kw):
    base = dict(
        as_of=datetime(2026, 5, 23, tzinfo=timezone.utc),
        company_health_score=80,
        runway_months=12.0,
        pending_approvals=0,
    )
    base.update(kw)
    return snapshot(**base)


def test_runway_p0_when_below_two_months():
    risks = RiskEngine().assess(_state(runway_months=1.0))
    assert any(r.severity == "P0" and r.code == "RUNWAY_P0" for r in risks)


def test_runway_p1_when_below_four_months():
    risks = RiskEngine().assess(_state(runway_months=3.0))
    assert any(r.severity == "P1" and r.code == "RUNWAY_P1" for r in risks)


def test_health_p0_at_score_30():
    risks = RiskEngine().assess(_state(company_health_score=30))
    assert any(r.code == "HEALTH_P0" for r in risks)


def test_approval_backlog_flagged():
    risks = RiskEngine().assess(_state(pending_approvals=10))
    assert any(r.code == "APPROVAL_BACKLOG" for r in risks)


def test_clean_state_has_no_p0_p1():
    risks = RiskEngine().assess(_state())
    assert not any(r.severity in {"P0", "P1"} for r in risks)

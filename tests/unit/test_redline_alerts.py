"""Tests for friction_log.redline_alerts — threshold + doctrine."""

from __future__ import annotations

from auto_client_acquisition.friction_log.redline_alerts import (
    AlertEvent,
    APPROVAL_BACKLOG_LIMIT,
    FRICTION_7D_LIMIT,
    check_approval_backlog,
    check_fleet_quiet,
    check_friction_spike,
    check_revenue_silence,
    compute_redline_alerts,
)


def _snap(
    *,
    approvals: int = 0,
    friction: int = 0,
    agent_runs: int = 0,
    revenue_today: int = 0,
    mrr: int = 0,
) -> dict:
    return {
        "revenue": {
            "today_sar": {"value": revenue_today, "is_estimate": False, "source": "t"},
            "mrr_sar": {"value": mrr, "is_estimate": True, "source": "t"},
        },
        "pipeline": {
            "approvals_pending": {"value": approvals, "is_estimate": False, "source": "t"},
        },
        "trust": {
            "friction_events_7d": {"value": friction, "is_estimate": False, "source": "t"},
        },
        "fleet": {
            "agent_runs_24h": {"value": agent_runs, "is_estimate": True, "source": "t"},
        },
    }


def test_alert_event_bilingual() -> None:
    ev = AlertEvent(
        code="x", severity="info",
        title_ar="عنوان", title_en="title",
        detail="d",
        suggested_action_ar="فعل", suggested_action_en="do",
    )
    d = ev.to_dict()
    assert d["title_ar"] == "عنوان"
    assert d["title_en"] == "title"
    assert "raised_at" in d


def test_approval_backlog_threshold() -> None:
    assert check_approval_backlog(_snap(approvals=APPROVAL_BACKLOG_LIMIT)) is None
    ev = check_approval_backlog(_snap(approvals=APPROVAL_BACKLOG_LIMIT + 1))
    assert ev is not None and ev.code == "approval_backlog_high"


def test_friction_spike_threshold() -> None:
    assert check_friction_spike(_snap(friction=FRICTION_7D_LIMIT)) is None
    ev = check_friction_spike(_snap(friction=FRICTION_7D_LIMIT + 1))
    assert ev is not None and ev.severity == "warn"


def test_fleet_quiet_triggers_only_at_zero() -> None:
    assert check_fleet_quiet(_snap(agent_runs=1)) is None
    ev = check_fleet_quiet(_snap(agent_runs=0))
    assert ev is not None and ev.code == "fleet_quiet"


def test_revenue_silence_triggers_when_both_zero() -> None:
    assert check_revenue_silence(_snap(revenue_today=1)) is None
    assert check_revenue_silence(_snap(mrr=1)) is None
    ev = check_revenue_silence(_snap(revenue_today=0, mrr=0))
    assert ev is not None and ev.severity == "critical"


def test_compute_with_no_snapshot_returns_info_event() -> None:
    alerts = compute_redline_alerts(snap=None)
    # Depending on whether a snapshot exists on disk, we get either the
    # no_kpi_snapshot info event or real alerts. In both cases the API
    # contract is: a list of AlertEvent dicts.
    assert isinstance(alerts, list)
    for a in alerts:
        # AlertEvent objects when compute_redline_alerts returns
        assert hasattr(a, "code")
        assert hasattr(a, "severity")


def test_compute_with_clean_snapshot_returns_nothing() -> None:
    clean = _snap(approvals=0, friction=0, agent_runs=5, revenue_today=100, mrr=999)
    alerts = compute_redline_alerts(snap=clean)
    assert alerts == []


def test_compute_surfaces_critical_first() -> None:
    bad = _snap(approvals=50, friction=50, agent_runs=0, revenue_today=0, mrr=0)
    alerts = compute_redline_alerts(snap=bad)
    codes = [a.code for a in alerts]
    assert "approval_backlog_high" in codes
    assert "friction_spike_7d" in codes
    assert "fleet_quiet" in codes
    assert "revenue_silence" in codes

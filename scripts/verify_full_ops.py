#!/usr/bin/env python3
"""Verify the full Dealix Company OS by smoke-running each engine.

This goes beyond file-presence: it imports each control-plane module and
exercises a minimal call. Any exception fails the check.
"""

from __future__ import annotations

import sys
import traceback
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def check(name: str, fn) -> tuple[str, bool, str]:
    try:
        fn()
        return (name, True, "ok")
    except Exception:
        return (name, False, traceback.format_exc(limit=3))


def _company_state():
    from control_plane.company_state import CompanyState

    s = CompanyState()
    assert s.revenue.cash_collected == 0.0
    assert s.trust.a3_blocked_actions == 0
    assert isinstance(s.to_dict(), dict)


def _metrics_collector():
    from control_plane.metrics_collector import MetricsCollector

    state = MetricsCollector().collect(
        {
            "revenue": {"cash_collected": 1000, "mrr": 500, "proposals_pending": 2},
            "sales": {"leads_new": 25, "dms_due": 25, "replies": 3, "calls_booked": 1},
            "trust": {"approvals_waiting": 2},
        }
    )
    assert state.revenue.cash_collected == 1000.0
    assert state.sales.leads_new == 25
    assert state.trust.approvals_waiting == 2


def _ceo_brief():
    from control_plane.ceo_brief import render_daily_brief
    from control_plane.company_state import CompanyState

    md = render_daily_brief(CompanyState(), focus="Send 25 DMs.")
    assert "Daily CEO Brief" in md
    assert "Send 25 DMs." in md


def _decision_engine():
    from control_plane.decision_engine import DecisionEngine, DecisionInput, DecisionType

    eng = DecisionEngine()
    out = eng.classify(
        DecisionInput(
            title="Add payment fallback",
            revenue_impact=9,
            urgency=8,
            risk_reduction=9,
            founder_leverage=6,
            complexity=4,
        )
    )
    assert out.decision in {DecisionType.FIX, DecisionType.BUILD}

    rej = eng.classify(
        DecisionInput(
            title="Auto-sign NDA",
            revenue_impact=8,
            urgency=8,
            risk_reduction=2,
            founder_leverage=5,
            complexity=2,
            trust_violation=True,
        )
    )
    assert rej.decision == DecisionType.REJECT


def _approval_router():
    from control_plane.approval_router import ApprovalLevel, ApprovalRouter

    r = ApprovalRouter()
    assert r.route("lead_scoring").level == ApprovalLevel.A0
    assert r.route("proposal_send").level == ApprovalLevel.A2
    assert r.route("refund").level == ApprovalLevel.A3
    # Unknown action must default to A2, not A0.
    assert r.route("something_new").level == ApprovalLevel.A2
    assert not r.is_auto_executable("refund")


def _risk_engine():
    from control_plane.risk_engine import RiskEngine, RiskSignals, RiskSeverity

    risks = RiskEngine().evaluate(
        RiskSignals(
            payment_fallback_missing=True,
            public_repo_contains_leads=True,
            ci_failing_on_main=True,
        )
    )
    severities = {r.severity for r in risks}
    assert RiskSeverity.CRITICAL in severities
    assert RiskSeverity.HIGH in severities


def _system_scorecard():
    from control_plane.system_scorecard import SystemScorecard, SystemStatus

    sc = SystemScorecard()
    sc.set_score("Revenue OS", 92, "docs/revenue/", "Hold the line")
    sc.set_score("Trust OS", 95, "docs/trust/", "Hold the line")
    assert sc.aggregate() >= 50
    assert sc.aggregate_status() in {
        SystemStatus.PASS,
        SystemStatus.READY_INTERNAL,
        SystemStatus.FIX,
        SystemStatus.BLOCKED,
    }


def _learning_router():
    from control_plane.learning_router import LearningRouter, LearningDecision

    out = LearningRouter().route({"dms": 25, "replies": 1})
    assert any(o.decision == LearningDecision.FIX for o in out)


CHECKS = [
    ("company_state", _company_state),
    ("metrics_collector", _metrics_collector),
    ("ceo_brief", _ceo_brief),
    ("decision_engine", _decision_engine),
    ("approval_router", _approval_router),
    ("risk_engine", _risk_engine),
    ("system_scorecard", _system_scorecard),
    ("learning_router", _learning_router),
]


def main() -> int:
    results = [check(name, fn) for name, fn in CHECKS]
    failed = [r for r in results if not r[1]]

    for name, ok, msg in results:
        marker = "PASS" if ok else "FAIL"
        print(f"[{marker}] {name}")
        if not ok:
            print(msg)

    if failed:
        print(f"[FAIL] {len(failed)}/{len(results)} full-ops checks failed.")
        return 1

    print(f"[PASS] {len(results)}/{len(results)} full-ops checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

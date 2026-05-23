#!/usr/bin/env python3
"""
verify_company_os.py — end-to-end smoke test of the Company OS.

Builds a synthetic CompanyState, drives it through the control plane
(decision engine, action router, approval router, risk engine), and the
operating intelligence layer (priority engine, bottleneck, weekly
review). Asserts every stage produces the expected shape.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from control_plane import (  # noqa: E402
    ApprovalRouter, ActionRouter, DecisionEngine, RiskEngine,
    generate_ceo_brief, snapshot,
)
from operating_intelligence import (  # noqa: E402
    BottleneckDetector, LearningSynthesizer, PriorityEngine,
    generate_weekly_review,
)


def main() -> int:
    state = snapshot(
        as_of=datetime(2026, 5, 23, tzinfo=timezone.utc),
        stage="0-founder-clarity",
        leads_this_week=12,
        qualified_leads=3,
        proposals_out=0,
        paid_sprints=0,
        cash_collected_30d=2500.0,
        mrr=0.0,
        runway_months=3.5,
        pending_approvals=2,
        open_risks=["lead-pipeline thin"],
        company_health_score=55,
    )
    if state.is_healthy:
        print("[FAIL] healthy state should not be healthy at score 55")
        return 1

    brief = generate_ceo_brief(state)
    if "Daily CEO Brief" not in brief.title or "ALERT" not in brief.body:
        print("[FAIL] brief missing alert band")
        return 1

    engine = DecisionEngine()
    decisions = engine.propose(state)
    if not decisions:
        print("[FAIL] decision engine returned no decisions")
        return 1

    router = ActionRouter()
    routed = [router.route(d) for d in decisions]
    if not any(r.destination in {"workflow", "approval_queue"} for r in routed):
        print("[FAIL] action router produced no valid routes")
        return 1

    approvals = ApprovalRouter()
    for r in routed:
        if r.destination == "approval_queue":
            approvals.submit(r.decision.label, r.decision.approval_class)
    if len(approvals.pending()) == 0 and any(r.destination == "approval_queue" for r in routed):
        print("[FAIL] approval router did not record pending items")
        return 1

    risks = RiskEngine().assess(state)
    if not risks:
        print("[FAIL] risk engine produced no risks for state with 3.5 mo runway")
        return 1

    pe = PriorityEngine()
    ranked = pe.rank([pe.score(label=d.label, impact=4, leverage=3, reversibility=4) for d in decisions])
    if ranked != sorted(ranked, key=lambda x: x.score, reverse=True):
        print("[FAIL] priority engine did not sort")
        return 1

    bd = BottleneckDetector()
    bottleneck = bd.detect({
        "lead_to_qualified": 0.20,
        "qualified_to_proposal": 0.10,
        "proposal_to_paid": 0.00,
        "paid_to_renewed": 0.00,
    })
    if bottleneck is None:
        print("[FAIL] bottleneck detector failed on a clearly broken funnel")
        return 1

    learning = LearningSynthesizer().summarize([], period="2026-W21")
    review = generate_weekly_review(state, bottleneck=bottleneck, learning=learning)
    if "Weekly CEO Review" not in review.title:
        print("[FAIL] weekly review title malformed")
        return 1

    print("[OK] verify_company_os: end-to-end smoke passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
verify_control_plane.py — assert each control_plane module's public API works.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from control_plane.action_router import ActionRouter  # noqa: E402
from control_plane.approval_router import ApprovalRouter  # noqa: E402
from control_plane.ceo_brief import generate_ceo_brief  # noqa: E402
from control_plane.company_state import snapshot  # noqa: E402
from control_plane.decision_engine import DecisionEngine  # noqa: E402
from control_plane.learning_router import LearningRouter  # noqa: E402
from control_plane.metrics_collector import MetricsCollector  # noqa: E402
from control_plane.risk_engine import RiskEngine  # noqa: E402
from control_plane.system_scorecard import score_system  # noqa: E402


def main() -> int:
    failures: list[str] = []

    state = snapshot(
        as_of=datetime(2026, 5, 23, tzinfo=timezone.utc),
        leads_this_week=10,
        runway_months=1.0,
        company_health_score=30,
        pending_approvals=6,
    )

    brief = generate_ceo_brief(state)
    if "ALERT" not in brief.body:
        failures.append("ceo_brief did not flag alert band for score=30")

    decisions = DecisionEngine().propose(state)
    if not decisions:
        failures.append("decision_engine returned no decisions")

    router = ActionRouter()
    routed = [router.route(d) for d in decisions]
    if not any(r.destination in {"workflow", "approval_queue"} for r in routed):
        failures.append("action_router produced no routes")

    approvals = ApprovalRouter()
    approvals.submit("test_action", "founder")
    approvals.resolve(approvals.pending()[0].id, approved=True, reason="smoke")
    stats = approvals.stats()
    if stats.get("approved", 0) != 1:
        failures.append(f"approval_router approved stat wrong: {stats}")

    risks = RiskEngine().assess(state)
    severities = {r.severity for r in risks}
    if "P0" not in severities:
        failures.append(f"risk_engine should flag P0 at runway 1.0: got {severities}")

    metrics = MetricsCollector()
    metrics.incr("leads", 5)
    metrics.gauge("health", 30.0)
    snap = metrics.snapshot()
    if snap["counters"].get("leads") != 5 or snap["gauges"].get("health") != 30.0:
        failures.append(f"metrics_collector wrong: {snap}")

    sc = score_system("trust", signals={"audit": 0.9, "approvals": 0.7})
    if not 0 <= sc.score <= 100:
        failures.append(f"system_scorecard out of range: {sc.score}")

    routed_kind = LearningRouter().route(LearningRouter().capture("win", "first sprint"))
    if not routed_kind.endswith("win_loss_review.md"):
        failures.append(f"learning_router wrong destination: {routed_kind}")

    if failures:
        print(f"[FAIL] verify_control_plane: {len(failures)} issues")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("[OK] verify_control_plane: all subsystems wired correctly")
    return 0


if __name__ == "__main__":
    sys.exit(main())

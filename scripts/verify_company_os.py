#!/usr/bin/env python3
"""Verify that the 12 Dealix Company OS systems have their core files.

Each system is scored as the percentage of required files that exist and
are non-empty. Status bands match DEALIX_COMPANY_OS_SCORECARD.md.

Exit code:
- 0 when overall health is >= 50 (FIX or better)
- 1 when overall health is < 50 (BLOCKED)

The CI gate uses --strict to fail when any single system is BLOCKED.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

SYSTEMS: dict[str, list[str]] = {
    "founder": [
        "docs/founder/CEO_OPERATING_SYSTEM.md",
        "docs/founder/DAILY_COMMAND_BRIEF.md",
        "docs/founder/WEEKLY_CEO_REVIEW.md",
        "docs/founder/DECISION_LOG.md",
        "docs/founder/RISK_REGISTER.md",
        "docs/founder/FOCUS_POLICY.md",
        "docs/founder/COMPANY_HEALTH_SCORE.md",
        "docs/founder/CEO_DASHBOARD_SPEC.md",
    ],
    "strategy": [
        "docs/strategy/NORTH_STAR.md",
        "docs/strategy/STRATEGIC_THESIS.md",
        "docs/strategy/ICP_STRATEGY.md",
        "docs/strategy/GTM_STRATEGY.md",
        "docs/strategy/COMPETITIVE_STRATEGY.md",
        "docs/strategy/MOAT_STRATEGY.md",
        "docs/strategy/PRICING_STRATEGY.md",
        "docs/strategy/90_DAY_PLAN.md",
    ],
    "revenue": [
        "docs/revenue/REVENUE_MODEL.md",
        "docs/revenue/OFFER_LADDER.md",
        "docs/revenue/PIPELINE_STAGES.md",
        "docs/revenue/REVENUE_METRICS.md",
        "docs/revenue/CASH_RULES.md",
        "docs/revenue/PROPOSAL_RULES.md",
        "docs/revenue/PRICING_EXPERIMENTS.md",
        "docs/revenue/WIN_LOSS_REVIEW.md",
    ],
    "acquisition": [
        "docs/strategy/GTM_STRATEGY.md",
        "docs/strategy/MARKET_MAP_SAUDI.md",
        "docs/strategy/ICP_STRATEGY.md",
    ],
    "sales": [
        "docs/revenue/PIPELINE_STAGES.md",
        "docs/revenue/PROPOSAL_RULES.md",
        "docs/revenue/OFFER_LADDER.md",
    ],
    "delivery": [
        "docs/revenue/PROPOSAL_RULES.md",
        "docs/agents/AGENT_HANDOFFS.md",
    ],
    "trust": [
        "docs/trust/APPROVAL_MATRIX.md",
        "docs/trust/NO_OVERCLAIM_POLICY.md",
        "docs/trust/AI_GOVERNANCE.md",
        "docs/trust/AGENT_BOUNDARIES.md",
        "docs/trust/WORKFLOW_RISK_CLASSIFICATION.md",
        "docs/trust/HUMAN_APPROVAL_POLICY.md",
    ],
    "finance": [
        "docs/revenue/CASH_RULES.md",
        "docs/revenue/REVENUE_METRICS.md",
    ],
    "client_success": [
        "docs/agents/AGENT_HANDOFFS.md",
        "docs/revenue/WIN_LOSS_REVIEW.md",
    ],
    "product": [
        "DEALIX_OPERATING_DOCTRINE.md",
        "DEALIX_COMPANY_OS_SCORECARD.md",
    ],
    "content": [
        "docs/trust/NO_OVERCLAIM_POLICY.md",
    ],
    "learning": [
        "docs/learning/EXPERIMENT_LOG.md",
        "docs/learning/WIN_LOSS_REVIEW.md",
        "docs/learning/MESSAGE_PERFORMANCE.md",
        "docs/learning/SECTOR_PERFORMANCE.md",
        "docs/learning/PRICING_LEARNING.md",
        "docs/learning/AGENT_EVALS.md",
        "docs/learning/MONTHLY_STRATEGY_UPDATE.md",
    ],
}


def file_ok(rel_path: str) -> tuple[bool, str]:
    path = REPO_ROOT / rel_path
    if not path.exists():
        return False, "missing"
    if path.stat().st_size == 0:
        return False, "empty"
    return True, "ok"


def score_system(files: list[str]) -> tuple[int, list[dict]]:
    detail = []
    passing = 0
    for f in files:
        ok, reason = file_ok(f)
        detail.append({"file": f, "status": reason})
        if ok:
            passing += 1
    score = round((passing / len(files)) * 100) if files else 0
    return score, detail


def status_for(score: int) -> str:
    if score >= 90:
        return "PASS"
    if score >= 75:
        return "READY_INTERNAL"
    if score >= 50:
        return "FIX"
    return "BLOCKED"


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Dealix Company OS")
    parser.add_argument(
        "--json", action="store_true", help="Emit machine-readable JSON output"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail (exit 1) when any single system is BLOCKED",
    )
    args = parser.parse_args()

    results: dict[str, dict] = {}
    total = 0
    for system, files in SYSTEMS.items():
        score, detail = score_system(files)
        total += score
        results[system] = {
            "score": score,
            "status": status_for(score),
            "files": detail,
        }

    health = round(total / len(SYSTEMS)) if SYSTEMS else 0
    overall_status = status_for(health)

    if args.json:
        print(
            json.dumps(
                {
                    "company_health": health,
                    "company_status": overall_status,
                    "systems": results,
                },
                indent=2,
            )
        )
    else:
        print("Dealix Company OS Verification")
        print("=" * 60)
        for name, data in results.items():
            print(f"  {name:<16} {data['score']:>3} {data['status']}")
            for f in data["files"]:
                if f["status"] != "ok":
                    print(f"      - {f['file']}: {f['status']}")
        print("-" * 60)
        print(f"  COMPANY HEALTH   {health:>3} {overall_status}")

    if args.strict:
        blocked = [n for n, d in results.items() if d["status"] == "BLOCKED"]
        if blocked:
            sys.stderr.write(
                f"FAIL: BLOCKED systems: {', '.join(blocked)}\n"
            )
            return 1

    return 0 if health >= 50 else 1


if __name__ == "__main__":
    raise SystemExit(main())

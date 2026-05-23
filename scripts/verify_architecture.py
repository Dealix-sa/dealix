#!/usr/bin/env python3
"""
verify_architecture.py — assert the architectural skeleton is intact.

Imports key packages and verifies the public symbols they advertise are
importable. Fails fast if a critical module disappeared.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))


REQUIRED_IMPORTS = [
    # control plane
    ("control_plane", [
        "CompanyState", "snapshot",
        "CEOBrief", "generate_ceo_brief",
        "Decision", "DecisionEngine",
        "ActionRouter", "RoutedAction",
        "ApprovalRouter", "PendingApproval",
        "RiskEngine", "RiskItem",
        "MetricsCollector",
        "SystemScorecard", "score_system",
        "LearningRouter", "LearningSignal",
    ]),
    # operating intelligence
    ("operating_intelligence", [
        "OperatingSignal", "collect_signals",
        "PriorityEngine", "PrioritizedItem",
        "BottleneckDetector", "Bottleneck",
        "OpportunityDetector", "Opportunity",
        "prioritize_risks",
        "LearningSynthesizer", "LearningSummary",
        "WeeklyReview", "generate_weekly_review",
        "MonthlyStrategy", "generate_monthly_strategy",
        "SystemImprovementPlanner", "ImprovementProposal",
    ]),
    # trust modules created by the Master Tree
    ("dealix.trust.approval_matrix", ["ApprovalMatrix", "ActionPolicy"]),
    ("dealix.trust.claim_guard", ["ClaimGuard", "ClaimViolation"]),
    ("dealix.trust.suppression", ["SuppressionList"]),
    ("dealix.trust.public_safety", ["scan", "is_safe", "PublicSafetyFinding"]),
    ("dealix.trust.autonomy_policy", ["evaluate", "AutonomyDecision"]),
    ("dealix.trust.policy_engine", ["PolicyEngine", "PolicyResult"]),
    ("dealix.trust.data_retention", ["policy", "evaluate", "RetentionDecision"]),
    ("dealix.trust.evidence_pack", ["EvidencePack", "new_pack"]),
    ("dealix.trust.incident_response", ["Incident", "new_incident"]),
]


def main() -> int:
    failures: list[str] = []
    for module_name, expected in REQUIRED_IMPORTS:
        try:
            mod = importlib.import_module(module_name)
        except Exception as exc:
            failures.append(f"import {module_name}: {exc!r}")
            continue
        for symbol in expected:
            if not hasattr(mod, symbol):
                failures.append(f"{module_name} missing symbol {symbol}")

    if failures:
        print(f"[FAIL] verify_architecture: {len(failures)} issues")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"[OK] verify_architecture: {len(REQUIRED_IMPORTS)} modules wired correctly")
    return 0


if __name__ == "__main__":
    sys.exit(main())

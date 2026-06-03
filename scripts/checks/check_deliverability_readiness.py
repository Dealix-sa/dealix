"""
check_deliverability_readiness.py — verify deliverability reviews and suppression policy.

Run from repo root:
    python scripts/checks/check_deliverability_readiness.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent

REQUIRED_FILES: list[tuple[str, str]] = [
    (
        "reports/deliverability/DAILY_DELIVERABILITY_REVIEW.md",
        "DAILY_DELIVERABILITY_REVIEW",
    ),
    (
        "reports/deliverability/DOMAIN_HEALTH_REVIEW.md",
        "DOMAIN_HEALTH_REVIEW",
    ),
    (
        "docs/privacy/DO_NOT_CONTACT_AND_SUPPRESSION_POLICY_AR.md",
        "DO_NOT_CONTACT_AND_SUPPRESSION_POLICY",
    ),
]


def run_checks() -> int:
    """Run all deliverability readiness checks. Returns count of failures."""
    print("=" * 60)
    print("CHECK: deliverability readiness")
    print("=" * 60)

    failures = 0
    for rel, label in REQUIRED_FILES:
        path = REPO_ROOT / rel
        if path.exists():
            print(f"  PASS  {label}: file found")
        else:
            print(f"  FAIL  {label}: file not found at {rel}")
            failures += 1

    total = len(REQUIRED_FILES)
    passed = total - failures
    print("-" * 60)
    print(f"Summary: {passed}/{total} passed, {failures} failed")
    return failures


def main() -> None:
    failures = run_checks()
    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()

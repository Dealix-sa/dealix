"""
check_delivery_gate.py — verify delivery pipeline status, blockers, and doc presence.

Run from repo root:
    python scripts/checks/check_delivery_gate.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent

REQUIRED_FILES: list[tuple[str, str]] = [
    (
        "reports/delivery/DELIVERY_PIPELINE_STATUS.md",
        "DELIVERY_PIPELINE_STATUS",
    ),
    (
        "reports/delivery/DELIVERY_BLOCKERS.md",
        "DELIVERY_BLOCKERS",
    ),
    (
        "docs/delivery/AUTOMATED_DELIVERY_PIPELINE_AR.md",
        "AUTOMATED_DELIVERY_PIPELINE",
    ),
    (
        "docs/delivery/CLIENT_DELIVERY_ACCEPTANCE_SYSTEM_AR.md",
        "CLIENT_DELIVERY_ACCEPTANCE_SYSTEM",
    ),
]


def run_checks() -> int:
    """Run all delivery gate checks. Returns count of failures."""
    print("=" * 60)
    print("CHECK: delivery gate")
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

"""
check_client_delivery_acceptance.py — verify sign-off queue, sign-off template, and value reports.

Run from repo root:
    python scripts/checks/check_client_delivery_acceptance.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent

REQUIRED_FILES: list[tuple[str, str]] = [
    (
        "reports/delivery/CLIENT_SIGN_OFF_QUEUE.md",
        "CLIENT_SIGN_OFF_QUEUE",
    ),
    (
        "docs/delivery/DELIVERY_SIGN_OFF_TEMPLATE_AR.md",
        "DELIVERY_SIGN_OFF_TEMPLATE",
    ),
    (
        "reports/delivery/WEEKLY_VALUE_REPORT_QUEUE.md",
        "WEEKLY_VALUE_REPORT_QUEUE",
    ),
]


def run_checks() -> int:
    """Run all client delivery acceptance checks. Returns count of failures."""
    print("=" * 60)
    print("CHECK: client delivery acceptance")
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

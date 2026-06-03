"""
check_account_pack_contract.py — verify account queue and allowed-use policy.

Run from repo root:
    python scripts/checks/check_account_pack_contract.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent

ACCOUNT_QUEUE_PATH = REPO_ROOT / "reports/account_intelligence/TOP_100_ACCOUNT_QUEUE.md"
ALLOWED_USE_PATH = REPO_ROOT / "docs/04_data_os/ALLOWED_USE_POLICY.md"

REQUIRED_COLUMNS = ["company_name", "sector", "need_fit_score", "NeedFit"]


def _check_account_queue() -> tuple[int, int]:
    """
    Check account queue exists and has required columns.
    Returns (failures, total_checks).
    """
    rel = ACCOUNT_QUEUE_PATH.relative_to(REPO_ROOT)
    if not ACCOUNT_QUEUE_PATH.exists():
        print(f"  FAIL  ACCOUNT_QUEUE: file not found at {rel}")
        return 1, 1

    content = ACCOUNT_QUEUE_PATH.read_text(encoding="utf-8", errors="replace")
    # Require company_name AND sector both present
    missing = []
    for field in ("company_name", "sector"):
        if field.lower() not in content.lower():
            missing.append(field)

    # Require at least one score column
    has_score = any(col.lower() in content.lower() for col in ("need_fit_score", "needfit"))

    failures = 0
    checks = 0

    checks += 1
    print(f"  PASS  ACCOUNT_QUEUE: file found")

    checks += 1
    if missing:
        print(f"  FAIL  ACCOUNT_QUEUE: missing required columns: {missing}")
        failures += 1
    else:
        print("  PASS  ACCOUNT_QUEUE: 'company_name' and 'sector' columns present")

    checks += 1
    if has_score:
        print("  PASS  ACCOUNT_QUEUE: score column (need_fit_score / NeedFit) present")
    else:
        print("  FAIL  ACCOUNT_QUEUE: no score column found (need_fit_score or NeedFit)")
        failures += 1

    return failures, checks


def run_checks() -> int:
    """Run all account pack contract checks. Returns count of failures."""
    print("=" * 60)
    print("CHECK: account pack contract")
    print("=" * 60)

    failures = 0
    total = 0

    queue_failures, queue_total = _check_account_queue()
    failures += queue_failures
    total += queue_total

    # Allowed use policy
    total += 1
    rel = ALLOWED_USE_PATH.relative_to(REPO_ROOT)
    if ALLOWED_USE_PATH.exists():
        print(f"  PASS  ALLOWED_USE_POLICY: file found at {rel}")
    else:
        print(f"  FAIL  ALLOWED_USE_POLICY: file not found at {rel}")
        failures += 1

    passed = total - failures
    print("-" * 60)
    print(f"Summary: {passed}/{total} passed, {failures} failed")
    return failures


def main() -> None:
    failures = run_checks()
    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()

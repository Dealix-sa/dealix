"""
check_scale_readiness.py — verify scale scorecard and supporting review reports.

Run from repo root:
    python scripts/checks/check_scale_readiness.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent

SCALE_SCORECARD_PATH = REPO_ROOT / "reports/scale/ULTIMATE_SCALE_SCORECARD.md"
WEEKLY_SCALE_REVIEW_PATH = REPO_ROOT / "reports/scale/WEEKLY_SCALE_REVIEW.md"
DELIVERY_CAPACITY_PATH = REPO_ROOT / "reports/scale/DELIVERY_CAPACITY_REVIEW.md"

_SCORE_PATTERN = re.compile(
    r"(?:score[:\s]+|total[:\s]+)?(\d{1,3})\s*(?:/\s*100|%|\.0)?",
    re.IGNORECASE,
)


def _extract_score(content: str) -> int | None:
    """Return the first plausible 0-100 integer found in content, or None."""
    for match in _SCORE_PATTERN.finditer(content):
        value = int(match.group(1))
        if 0 <= value <= 100:
            return value
    return None


def run_checks() -> int:
    """Run all scale readiness checks. Returns count of failures."""
    print("=" * 60)
    print("CHECK: scale readiness")
    print("=" * 60)

    failures = 0
    total = 0

    # Scale scorecard
    total += 1
    if not SCALE_SCORECARD_PATH.exists():
        rel = SCALE_SCORECARD_PATH.relative_to(REPO_ROOT)
        print(f"  FAIL  ULTIMATE_SCALE_SCORECARD: file not found at {rel}")
        failures += 1
    else:
        print(f"  PASS  ULTIMATE_SCALE_SCORECARD: file found")
        content = SCALE_SCORECARD_PATH.read_text(encoding="utf-8", errors="replace")
        total += 1
        score = _extract_score(content)
        if score is None:
            print("  FAIL  ULTIMATE_SCALE_SCORECARD: no numeric score (0-100) found")
            failures += 1
        else:
            print(f"  PASS  ULTIMATE_SCALE_SCORECARD: scale score = {score}")

    # Weekly scale review
    total += 1
    if WEEKLY_SCALE_REVIEW_PATH.exists():
        print(f"  PASS  WEEKLY_SCALE_REVIEW: file found")
    else:
        rel = WEEKLY_SCALE_REVIEW_PATH.relative_to(REPO_ROOT)
        print(f"  FAIL  WEEKLY_SCALE_REVIEW: file not found at {rel}")
        failures += 1

    # Delivery capacity review
    total += 1
    if DELIVERY_CAPACITY_PATH.exists():
        print(f"  PASS  DELIVERY_CAPACITY_REVIEW: file found")
    else:
        rel = DELIVERY_CAPACITY_PATH.relative_to(REPO_ROOT)
        print(f"  FAIL  DELIVERY_CAPACITY_REVIEW: file not found at {rel}")
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

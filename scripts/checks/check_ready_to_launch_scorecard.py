"""
check_ready_to_launch_scorecard.py — read LAUNCH_SCORECARD.md and report launch readiness tier.

Run from repo root:
    python scripts/checks/check_ready_to_launch_scorecard.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent

LAUNCH_SCORECARD_PATH = REPO_ROOT / "reports/launch/LAUNCH_SCORECARD.md"

# Tiers: (min_score, label)
TIERS: list[tuple[int, str]] = [
    (90, "Launch Ready"),
    (85, "Controlled Launch"),
    (75, "Soft Launch"),
    (60, "Dry Run"),
    (0, "Not Ready"),
]

# Regex to extract a score: looks for patterns like "Score: 87", "87/100", "87%", or a bare integer
_SCORE_PATTERN = re.compile(
    r"(?:score[:\s]+|total[:\s]+)?(\d{1,3})\s*(?:/\s*100|%|\.0)?",
    re.IGNORECASE,
)


def _classify_score(score: int) -> str:
    """Return the tier label for a given score."""
    for min_score, label in TIERS:
        if score >= min_score:
            return label
    return "Not Ready"


def _extract_score(content: str) -> int | None:
    """
    Try to extract the primary score from scorecard content.
    Returns the first plausible 0-100 integer found, or None.
    """
    for match in _SCORE_PATTERN.finditer(content):
        value = int(match.group(1))
        if 0 <= value <= 100:
            return value
    return None


def run_checks() -> int:
    """Run launch scorecard checks. Returns count of failures."""
    print("=" * 60)
    print("CHECK: ready-to-launch scorecard")
    print("=" * 60)

    failures = 0
    total = 0

    total += 1
    if not LAUNCH_SCORECARD_PATH.exists():
        rel = LAUNCH_SCORECARD_PATH.relative_to(REPO_ROOT)
        print(f"  FAIL  LAUNCH_SCORECARD: file not found at {rel}")
        failures += 1
        print("-" * 60)
        print(f"Summary: 0/{total} passed, {failures} failed")
        return failures

    print(f"  PASS  LAUNCH_SCORECARD: file found")

    content = LAUNCH_SCORECARD_PATH.read_text(encoding="utf-8", errors="replace")

    total += 1
    score = _extract_score(content)
    if score is None:
        print("  FAIL  LAUNCH_SCORECARD: no numeric score (0-100) found in file")
        failures += 1
    else:
        tier = _classify_score(score)
        print(f"  PASS  LAUNCH_SCORECARD: score = {score} — tier: {tier}")
        if score >= 90:
            print("        Recommendation: proceed to full launch")
        elif score >= 85:
            print("        Recommendation: launch with controlled rollout")
        elif score >= 75:
            print("        Recommendation: soft launch to limited accounts")
        elif score >= 60:
            print("        Recommendation: dry run only; address blockers first")
        else:
            print("        Recommendation: not ready — resolve all critical gaps")

    passed = total - failures
    print("-" * 60)
    print(f"Summary: {passed}/{total} passed, {failures} failed")
    return failures


def main() -> None:
    failures = run_checks()
    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()

"""
check_email_quality_gate.py — verify outreach playbook and email drafts, scan for banned phrases.

Run from repo root:
    python scripts/checks/check_email_quality_gate.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent

OUTREACH_PLAYBOOK_PATH = (
    REPO_ROOT / "docs/outreach/SYSTEM_BASED_OUTREACH_PLAYBOOK_AR.md"
)
EMAIL_DRAFTS_PATH = REPO_ROOT / "reports/outreach/SYSTEM_EMAIL_DRAFTS_REVIEW.md"

# Banned phrase patterns: (description, compiled_regex)
BANNED_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("guaranteed (EN)", re.compile(r"\bguaranteed\b", re.IGNORECASE)),
    # Arabic guarantee word in revenue context
    ("مضمون (AR revenue guarantee)", re.compile(r"مضمون", re.UNICODE)),
    # 100% followed by نجاح (success) within 40 chars
    (
        "100% نجاح (success guarantee)",
        re.compile(r"100\s*%[^.]{0,40}نجاح", re.UNICODE | re.IGNORECASE),
    ),
]


def _scan_for_banned(path: Path, label: str) -> int:
    """Scan a file for banned phrases. Returns count of banned-phrase failures."""
    content = path.read_text(encoding="utf-8", errors="replace")
    failures = 0
    for description, pattern in BANNED_PATTERNS:
        if pattern.search(content):
            print(f"  FAIL  {label}: banned phrase detected — '{description}'")
            failures += 1
        else:
            print(f"  PASS  {label}: no banned phrase '{description}'")
    return failures


def run_checks() -> int:
    """Run all email quality gate checks. Returns count of failures."""
    print("=" * 60)
    print("CHECK: email quality gate")
    print("=" * 60)

    failures = 0
    total = 0

    # Outreach playbook
    total += 1
    if OUTREACH_PLAYBOOK_PATH.exists():
        print(f"  PASS  OUTREACH_PLAYBOOK: file found")
        # Scan for banned phrases
        total += len(BANNED_PATTERNS)
        failures += _scan_for_banned(OUTREACH_PLAYBOOK_PATH, "OUTREACH_PLAYBOOK")
    else:
        print(
            f"  FAIL  OUTREACH_PLAYBOOK: file not found at "
            f"{OUTREACH_PLAYBOOK_PATH.relative_to(REPO_ROOT)}"
        )
        failures += 1

    # Email drafts review
    total += 1
    if EMAIL_DRAFTS_PATH.exists():
        print(f"  PASS  EMAIL_DRAFTS: file found")
        total += len(BANNED_PATTERNS)
        failures += _scan_for_banned(EMAIL_DRAFTS_PATH, "EMAIL_DRAFTS")
    else:
        print(
            f"  FAIL  EMAIL_DRAFTS: file not found at "
            f"{EMAIL_DRAFTS_PATH.relative_to(REPO_ROOT)}"
        )
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

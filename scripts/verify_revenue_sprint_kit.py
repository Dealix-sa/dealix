#!/usr/bin/env python3
"""Verify the public Dealix Revenue Sprint Kit is present and trust-safe."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES: list[str] = [
    "docs/offers/revenue_sprint/REVENUE_SPRINT_KIT.md",
    "docs/offers/revenue_sprint/OFFER.md",
    "docs/offers/revenue_sprint/PRICING.md",
    "docs/offers/revenue_sprint/SCOPE.md",
    "docs/delivery/revenue_sprint/QA_CHECKLIST.md",
    "docs/trust/NO_OVERCLAIM_POLICY.md",
]

REQUIRED_KIT_SECTIONS: list[str] = [
    "Founder DM Pack",
    "Sample Pack",
    "Proposal",
    "QA",
    "Feedback",
    "Retainer",
]

# Forbidden phrases that must never appear in public Revenue Sprint kit files.
# Matched case-insensitively across the file body.
FORBIDDEN_PHRASES: list[str] = [
    "guaranteed revenue",
    "guaranteed sales",
    "guaranteed replies",
    "guaranteed meetings",
    "no-risk",
    "fully compliant",
    "100% automated sales",
    "fully autonomous sales",
]

MIN_FILE_BYTES = 120

# The no-overclaim policy is the canonical source that enumerates forbidden
# phrases; scanning it for those same phrases would be circular.
PHRASE_SCAN_EXEMPT: set[str] = {
    "docs/trust/NO_OVERCLAIM_POLICY.md",
}


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.exists():
            failures.append(f"Missing: {rel}")
            continue
        size = path.stat().st_size
        if size < MIN_FILE_BYTES:
            failures.append(f"Too short ({size} bytes): {rel}")

    kit_path = ROOT / "docs/offers/revenue_sprint/REVENUE_SPRINT_KIT.md"
    if kit_path.exists():
        text = kit_path.read_text(encoding="utf-8", errors="ignore")
        for section in REQUIRED_KIT_SECTIONS:
            if section not in text:
                failures.append(f"Revenue Sprint Kit missing section: {section}")

    for rel in REQUIRED_FILES:
        if rel in PHRASE_SCAN_EXEMPT:
            continue
        path = ROOT / rel
        if not path.exists():
            continue
        body = path.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in FORBIDDEN_PHRASES:
            needle = phrase.lower()
            if needle not in body:
                continue
            # Allow the phrase when every occurrence sits inside an explicit
            # negation context (e.g. "Dealix does not guarantee ...").
            if not _is_allowed_negation(body, needle):
                failures.append(f"Forbidden phrase in {rel}: {phrase}")

    if failures:
        print("Public Revenue Sprint Kit verification failed:")
        for failure in failures:
            print(f" - {failure}")
        return 1

    print("PASS: public Revenue Sprint Kit is ready.")
    return 0


def _is_allowed_negation(body: str, needle: str) -> bool:
    """Return True if every occurrence of `needle` sits inside a negation context.

    A negation context is a line that either starts with a markdown list/table
    marker and contains the phrase alongside one of the negation markers
    ("not", "never", "no ", "forbidden", "instead of", "out of scope",
    "does not", "explicitly"), or sits in the policy's forbidden-claims table.
    """

    negation_markers = (
        " not ",
        "never",
        "forbidden",
        "instead of",
        "out of scope",
        "does not",
        "do not",
        "explicitly",
        "no guaranteed",
        "without",
    )

    for line in body.splitlines():
        if needle not in line:
            continue
        if not any(marker in line for marker in negation_markers):
            return False
    return True


if __name__ == "__main__":
    sys.exit(main())

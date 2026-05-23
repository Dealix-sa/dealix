#!/usr/bin/env python3
"""verify_done_for_you_acquisition.py — Pre-commit verifier for the OS.

Checks:
    - required docs / scripts exist and are non-trivial
    - outreach message library contains no banned phrases (guarantee, etc.)
    - batch CSVs in acquisition/lead_batches/ parse and carry required cols
    - approval queue files exist for each batch
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES: list[str] = [
    "docs/acquisition/DONE_FOR_YOU_ACQUISITION_OS.md",
    "docs/acquisition/CONTACT_DISCOVERY_POLICY.md",
    "docs/delivery/REVENUE_SPRINT_SAMPLE_TEMPLATE.md",
    "docs/revenue/PROPOSAL_TRIGGER_RULES.md",
    "scripts/score_lead_batch.py",
    "scripts/generate_outreach_for_batch.py",
    "scripts/build_outreach_send_queue.py",
    "acquisition/source_targets.csv",
    "acquisition/contact_discovery_queue.csv",
    "acquisition/outreach_messages/erp_crm_v1.md",
]

REQUIRED_BATCH_COLS = {
    "company",
    "sector",
    "website",
    "fit_score",
    "priority",
    "verification_status",
    "suggested_message_id",
    "approval_status",
}

BANNED_PHRASES = [
    "guarantee",
    "guaranteed",
    "promised meetings",
    "guaranteed revenue",
    "guaranteed sales",
    "guaranteed replies",
]


def check_required_files() -> list[str]:
    failures: list[str] = []
    for rel in REQUIRED_FILES:
        path = REPO_ROOT / rel
        if not path.exists():
            failures.append(f"missing: {rel}")
        elif path.stat().st_size < 80:
            failures.append(f"too short: {rel}")
    return failures


def check_message_library() -> list[str]:
    failures: list[str] = []
    library_dir = REPO_ROOT / "acquisition" / "outreach_messages"
    for md in library_dir.glob("*.md"):
        text = md.read_text(encoding="utf-8").lower()
        for phrase in BANNED_PHRASES:
            # Allow appearances inside an explicit policy block.
            if phrase in text and "copy rules" not in text.split(phrase, 1)[0][-200:].lower():
                # Treat any other occurrence as a violation.
                failures.append(f"banned phrase '{phrase}' in {md.name}")
                break
    return failures


def check_batches() -> list[str]:
    failures: list[str] = []
    batch_dir = REPO_ROOT / "acquisition" / "lead_batches"
    approvals_dir = REPO_ROOT / "acquisition" / "approvals"
    if not batch_dir.exists():
        return ["missing dir: acquisition/lead_batches"]
    for batch in batch_dir.glob("*.csv"):
        with batch.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            cols = set(reader.fieldnames or [])
            rows = list(reader)
        missing_cols = REQUIRED_BATCH_COLS - cols
        if missing_cols:
            failures.append(f"{batch.name}: missing cols {sorted(missing_cols)}")
        if not rows:
            failures.append(f"{batch.name}: empty")
        approval_file = approvals_dir / f"{batch.stem}.md"
        if not approval_file.exists():
            failures.append(f"missing approval file for {batch.name}")
    return failures


def main() -> int:
    failures = check_required_files() + check_message_library() + check_batches()
    if failures:
        print("FAIL: done-for-you acquisition verification")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("PASS: done-for-you acquisition verification")
    return 0


if __name__ == "__main__":
    sys.exit(main())

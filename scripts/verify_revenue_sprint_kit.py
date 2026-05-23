"""Verify the public Revenue Sprint Kit is complete and non-trivial."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KIT_DIR = REPO_ROOT / "docs" / "offers" / "revenue_sprint"

REQUIRED_FILES = (
    "REVENUE_SPRINT_KIT.md",
    "founder_dm_pack.md",
    "sample_pack_template.md",
    "proposal_fast_template.md",
    "client_intake.md",
    "delivery_report_template.md",
    "qa_checklist.md",
    "handoff_template.md",
    "feedback_request.md",
    "retainer_ask.md",
)

MIN_BYTES = 200


def main() -> None:
    print("== Revenue Sprint Kit ==")
    failures: list[str] = []
    for name in REQUIRED_FILES:
        path = KIT_DIR / name
        if not path.exists():
            failures.append(f"Missing kit file: {name}")
            continue
        size = path.stat().st_size
        if size < MIN_BYTES:
            failures.append(f"Kit file too short: {name} ({size} < {MIN_BYTES} bytes)")
    if failures:
        print("FAIL:")
        for f in failures:
            print(f"- {f}")
        sys.exit(1)
    print(f"PASS: Revenue Sprint Kit complete ({len(REQUIRED_FILES)} files).")


if __name__ == "__main__":
    main()

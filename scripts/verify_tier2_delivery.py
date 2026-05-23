"""Verify Stage 2 (Delivery) scaffolding.

Checks:
- docs/delivery/revenue_sprint/ has 11 required files.
- QA_CHECKLIST has scope, evidence, and no-overclaim sections.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DELIVERY_FILES = [
    "QA_CHECKLIST.md",
    "KICKOFF_NOTE_TEMPLATE.md",
    "SYNC_AGENDA_TEMPLATE.md",
    "WRAPUP_BRIEF_TEMPLATE.md",
    "SCORING_RULES.md",
    "CHANGE_REQUEST.md",
    "HANDOFF_CHECKLIST.md",
    "RETRO_TEMPLATE.md",
    "EVIDENCE_PACK.md",
    "AGENT_ASSIGNMENTS.md",
    "README.md",
]

QA_REQUIRED_SECTIONS = ["Scope", "Evidence", "No overclaim"]


def check_files() -> tuple[bool, list[str]]:
    base = REPO_ROOT / "docs" / "delivery" / "revenue_sprint"
    missing = [f for f in REQUIRED_DELIVERY_FILES if not (base / f).exists()]
    return (not missing, missing)


def check_qa_sections() -> tuple[bool, list[str]]:
    p = REPO_ROOT / "docs" / "delivery" / "revenue_sprint" / "QA_CHECKLIST.md"
    if not p.exists():
        return False, QA_REQUIRED_SECTIONS
    text = p.read_text(encoding="utf-8").lower()
    missing: list[str] = []
    for section in QA_REQUIRED_SECTIONS:
        if section.lower() not in text:
            missing.append(section)
    return (not missing, missing)


def main() -> int:
    failures: list[str] = []

    ok, missing = check_files()
    if ok:
        print(f"PASS docs/delivery/revenue_sprint/ — all {len(REQUIRED_DELIVERY_FILES)} files present")
    else:
        print(f"FAIL docs/delivery/revenue_sprint/ — missing: {missing}")
        failures.append("delivery_files")

    ok, missing_sections = check_qa_sections()
    if ok:
        print("PASS QA_CHECKLIST.md — scope/evidence/no-overclaim sections present")
    else:
        print(f"FAIL QA_CHECKLIST.md — missing sections: {missing_sections}")
        failures.append("qa_sections")

    if failures:
        print(f"\nverify_tier2_delivery: FAIL ({len(failures)} checks)")
        return 1
    print("\nverify_tier2_delivery: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

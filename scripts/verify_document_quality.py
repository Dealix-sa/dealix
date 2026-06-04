"""Verify document quality for the Dealix Master Content Pack.

This verifier enforces the Dealix Document Standard on the canonical
operating documents that make up the Master Content Pack. Legacy
runbooks, AR playbooks, and tactical docs are not part of the pack and
are not checked here — those evolve under their own owners.

Add a file to MASTER_PACK_FILES to require it to meet the standard.
"""

from pathlib import Path

REQUIRED_SECTIONS = [
    "## Purpose",
    "## Owner",
    "## Review Cadence",
    "## Inputs",
    "## Outputs",
    "## Rules",
    "## Metrics",
    "## Evidence",
]

MASTER_PACK_FILES = [
    "DEALIX_OPERATING_DOCTRINE.md",
    "DEALIX_COMPANY_OS_SCORECARD.md",
    "docs/ops/DOCUMENT_STANDARD.md",
    "docs/ops/OPERATING_LOOPS.md",
    "docs/founder/DAILY_COMMAND_BRIEF.md",
    "docs/revenue/OFFER_LADDER.md",
    "docs/revenue/PIPELINE_STAGES.md",
    "docs/trust/APPROVAL_MATRIX.md",
    "docs/trust/AUTONOMY_POLICY.md",
    "docs/delivery/revenue_sprint/DELIVERY_PLAYBOOK.md",
    "docs/delivery/revenue_sprint/QA_CHECKLIST.md",
    "docs/learning/WEEKLY_INTELLIGENCE_REVIEW.md",
    "docs/control_plane/COMPANY_STATE_SCHEMA.md",
]


def main() -> None:
    failures = []

    for file in MASTER_PACK_FILES:
        path = Path(file)

        if not path.exists():
            failures.append(f"Missing master pack file: {file}")
            continue

        if path.stat().st_size < 120:
            failures.append(f"Too short: {file}")
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")

        missing_sections = [s for s in REQUIRED_SECTIONS if s not in text]
        if missing_sections:
            failures.append(
                f"{file} missing sections: {', '.join(missing_sections)}"
            )

    if failures:
        print("Document quality failures:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print(
        f"PASS: all {len(MASTER_PACK_FILES)} Master Content Pack documents "
        "meet the Dealix document standard."
    )


if __name__ == "__main__":
    main()

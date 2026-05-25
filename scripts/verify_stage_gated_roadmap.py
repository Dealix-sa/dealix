"""Verify the stage-gated roadmap doc is complete and machine-checkable."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ROADMAP = REPO_ROOT / "DEALIX_STAGE_GATED_ROADMAP.md"

REQUIRED_SECTIONS = (
    "## Stages",
    "## Gate enforcement",
    "## What this roadmap is NOT",
)

REQUIRED_STAGES_TEXT = (
    "Pipeline",
    "Outreach",
    "Samples",
    "Proposal",
    "Payment Attempt",
    "Delivery",
    "Learning",
)


def main() -> None:
    print("== Stage-Gated Roadmap ==")
    failures: list[str] = []
    if not ROADMAP.exists():
        print(f"FAIL: Missing {ROADMAP.relative_to(REPO_ROOT)}")
        sys.exit(1)
    body = ROADMAP.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        if section not in body:
            failures.append(f"Section missing: {section}")
    for stage in REQUIRED_STAGES_TEXT:
        if stage not in body:
            failures.append(f"Stage missing from doc: {stage}")
    if "verify_stage_gated_roadmap.py" not in body:
        failures.append("Doc must reference its own verifier")
    if "verify_stage_evidence_automation.py" not in body:
        failures.append("Doc must reference verify_stage_evidence_automation.py")
    if failures:
        print("FAIL:")
        for f in failures:
            print(f"- {f}")
        sys.exit(1)
    print("PASS: Stage-gated roadmap complete.")


if __name__ == "__main__":
    main()

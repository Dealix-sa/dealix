"""Verify the stage / evidence automation contracts.

Checks that:
- All stages defined in the execution engine match the stages documented in
  DEALIX_STAGE_GATED_ROADMAP.md.
- Every documented stage has at least one evidence check in the scanner
  (except `setup`, which is verified by the master audit script itself).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

ROADMAP = REPO_ROOT / "DEALIX_STAGE_GATED_ROADMAP.md"

EXPECTED_STAGES = {
    "setup",
    "pipeline",
    "outreach",
    "samples",
    "proposal",
    "payment_attempt",
    "delivery",
    "learning",
}


def _stages_in_roadmap() -> set[str]:
    if not ROADMAP.exists():
        return set()
    body = ROADMAP.read_text(encoding="utf-8")
    # Match table rows like: | 1 | **Pipeline** | ...
    pattern = re.compile(r"\|\s*\d+\s*\|\s*\*\*([A-Za-z _-]+)\*\*")
    return {m.group(1).strip().lower().replace(" ", "_") for m in pattern.finditer(body)}


def main() -> None:
    print("== Stage / Evidence Automation ==")
    failures: list[str] = []

    from execution_engine.evidence_scanner import (  # noqa: E402
        STAGES,
        _CHECKS_BY_STAGE,
    )

    code_stages = set(STAGES)
    if code_stages != EXPECTED_STAGES:
        failures.append(
            f"execution_engine.STAGES != expected: extra={code_stages - EXPECTED_STAGES}, "
            f"missing={EXPECTED_STAGES - code_stages}"
        )

    doc_stages = _stages_in_roadmap()
    missing_in_doc = EXPECTED_STAGES - doc_stages - {"setup"}
    if missing_in_doc:
        failures.append(f"Roadmap missing stages: {sorted(missing_in_doc)}")

    for stage in EXPECTED_STAGES - {"setup"}:
        checks = _CHECKS_BY_STAGE.get(stage, ())
        if not checks:
            failures.append(f"No evidence check for stage: {stage}")

    if failures:
        print("FAIL:")
        for f in failures:
            print(f"- {f}")
        sys.exit(1)
    print("PASS: stage / evidence automation aligned.")


if __name__ == "__main__":
    main()

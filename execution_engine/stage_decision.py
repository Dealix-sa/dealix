from __future__ import annotations

"""Decide whether the founder can advance to the next stage."""

from datetime import date
from pathlib import Path
from typing import Any

from .evidence_checker import EvidenceCheck, check_evidence_for_stage
from .evidence_report_generator import generate_evidence_report
from .stage_checklist_updater import update_checklist
from .stage_reader import read_current_stage, write_current_stage


def can_advance(checks: list[EvidenceCheck]) -> tuple[bool, list[str]]:
    """Return (advanceable, blockers)."""
    blockers = [c.criterion for c in checks if c.status != "pass"]
    return (not blockers, blockers)


def advance_if_eligible(private_ops_path: Path) -> dict[str, Any]:
    """Run the full advance flow.

    Returns a dict with keys:
    - advanced: bool
    - new_stage: int | None
    - blockers: list[str]
    """
    private_ops_path = Path(private_ops_path)
    stage = read_current_stage(private_ops_path)
    stage_num = int(stage.get("stage", 0))

    checks = check_evidence_for_stage(private_ops_path, stage_num)
    update_checklist(private_ops_path, checks)
    generate_evidence_report(private_ops_path, checks)

    eligible, blockers = can_advance(checks)
    if not eligible:
        return {"advanced": False, "new_stage": None, "blockers": blockers}

    new_stage_num = stage_num + 1
    write_current_stage(
        private_ops_path,
        {
            "stage": new_stage_num,
            "started_at": date.today().isoformat(),
            "target_exit_date": "",
            "status": "in_progress",
        },
    )
    return {"advanced": True, "new_stage": new_stage_num, "blockers": []}

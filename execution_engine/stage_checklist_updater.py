from __future__ import annotations

"""Persist evidence checks to a CSV checklist on disk."""

import csv
from pathlib import Path

from .evidence_checker import EvidenceCheck

CHECKLIST_RELPATH = "stage/stage_exit_checklist.csv"
_HEADER = ["criterion", "status", "evidence", "next_action"]


def update_checklist(private_ops_path: Path, checks: list[EvidenceCheck]) -> Path:
    """Write the checklist CSV; returns the file path it wrote to."""
    private_ops_path = Path(private_ops_path)
    target = private_ops_path / CHECKLIST_RELPATH
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(_HEADER)
        for chk in checks:
            writer.writerow(
                [chk.criterion, chk.status, chk.evidence_path, chk.next_action]
            )
    return target

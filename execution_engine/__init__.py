"""Dealix execution engine.

Reads stage state from the private ops repo, scans for evidence that exit
criteria are met, and updates the stage checklist. The engine never sends
external messages and never charges customers — it only computes whether
the current stage is ready to advance.

See `DEALIX_STAGE_GATED_ROADMAP.md` for the stage definitions.
"""

from execution_engine.evidence_scanner import (
    EvidenceReport,
    ScanResult,
    scan_evidence,
)
from execution_engine.stage_checklist_updater import (
    ChecklistRow,
    load_checklist,
    update_checklist,
)

__all__ = [
    "EvidenceReport",
    "ScanResult",
    "scan_evidence",
    "ChecklistRow",
    "load_checklist",
    "update_checklist",
]

from __future__ import annotations

"""Execution engine for Dealix Company Architecture v1.0 (Stage 5).

Reads stage state from the private ops directory and decides whether the
founder can advance to the next stage.
"""

from .evidence_checker import EvidenceCheck, check_evidence_for_stage
from .stage_decision import advance_if_eligible, can_advance
from .stage_reader import read_current_stage, write_current_stage

# Public surface
__all__ = [
    "Stage",
    "StageExitChecklist",
    "EvidenceCheck",
    "evidence_check",
    "current_stage",
    "run_advance",
    "check_evidence_for_stage",
    "read_current_stage",
    "write_current_stage",
    "can_advance",
    "advance_if_eligible",
]


# Compatibility aliases used by the higher-level shell / CLI.
Stage = dict  # plain dict shape returned by read_current_stage
StageExitChecklist = list  # list[EvidenceCheck]
evidence_check = check_evidence_for_stage
current_stage = read_current_stage
run_advance = advance_if_eligible

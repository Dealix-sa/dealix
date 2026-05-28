"""Hermes — top-layer agent orchestrator for Dealix.

Hermes sits above dealix-pm and routes work to the existing Claude Code
sub-agents (engineer, content, sales, delivery) and the ACA agent fleet.
Every dispatch is doctrine-checked, audit-logged, and returns a
governance_decision per the Dealix Constitution and Hermes Charter
(docs/institutional/HERMES_CHARTER.md).
"""

from __future__ import annotations

from .audit import HermesAuditRecord
from .governance_gate import GovernanceDecision, GovernanceGate
from .identity import HermesIdentity, new_run_id
from .orchestrator import HermesOrchestrator, HermesTask, HermesTaskResult
from .router import HermesRouter, TaskClass

__all__ = [
    "GovernanceDecision",
    "GovernanceGate",
    "HermesAuditRecord",
    "HermesIdentity",
    "HermesOrchestrator",
    "HermesRouter",
    "HermesTask",
    "HermesTaskResult",
    "TaskClass",
    "new_run_id",
]

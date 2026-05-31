"""Dealix Revenue + Customer Ops Autopilot — deterministic core.

Persistence defaults to ``var/revenue_ops_autopilot.json`` (gitignored).
No live external sends; high-impact actions enqueue approvals only.
"""

from dealix.revenue_ops_autopilot.orchestrator import RevenueAutopilotOrchestrator
from dealix.revenue_ops_autopilot.store import get_autopilot_store
from dealix.revenue_ops_autopilot.scoring import compute_lead_score, suggested_stage_from_score

__all__ = [
    "RevenueAutopilotOrchestrator",
    "get_autopilot_store",
    "compute_lead_score",
    "suggested_stage_from_score",
]

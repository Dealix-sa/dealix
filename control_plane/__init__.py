"""Dealix Autonomous Company Control Plane.

This package is the management layer above Dealix's twelve operating systems
(Founder, Strategy, Revenue, Acquisition, Sales, Delivery, Trust, Finance,
Client Success, Product, Content, Learning). It collects state, evaluates
decisions, routes approvals, raises risks, scores systems, and emits the
daily CEO brief.

See `docs/control_plane/` for architecture and contracts.
"""

from control_plane.company_state import CompanyState
from control_plane.decision_engine import DecisionEngine, DecisionType
from control_plane.approval_router import ApprovalRouter, ApprovalLevel
from control_plane.risk_engine import RiskEngine, RiskSeverity
from control_plane.system_scorecard import SystemScorecard, SystemStatus

__all__ = [
    "CompanyState",
    "DecisionEngine",
    "DecisionType",
    "ApprovalRouter",
    "ApprovalLevel",
    "RiskEngine",
    "RiskSeverity",
    "SystemScorecard",
    "SystemStatus",
]

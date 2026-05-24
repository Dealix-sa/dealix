"""
Sovereign Value Control Plane — §81–§110.

The Sovereign Control Plane is the top-of-stack governance layer that
keeps Sami in charge of every value-bearing decision while letting
agents, tools, and partners do work. It complements (does not replace)
the kernel's PolicyEvaluator and ApprovalGate.

This package is import-safe from anywhere inside ``dealix/`` but MUST
NOT depend on ``api/``, ``core/``, ``auto_client_acquisition/``, or
``autonomous_growth/``.
"""

from __future__ import annotations

from dealix.sovereign_control_plane.control_plane import (
    SovereignControlPlane,
    get_control_plane,
)
from dealix.sovereign_control_plane.types import (
    ApprovalDecision,
    DataSensitivity,
    IdentityKind,
    IncidentSeverity,
    IncidentType,
    OfferState,
    RiskLevel,
    RunStatus,
    SecurityMode,
    SovereigntyLevel,
    ToolCallStatus,
    WorkspaceType,
)

__all__ = [
    "SovereignControlPlane",
    "get_control_plane",
    "ApprovalDecision",
    "DataSensitivity",
    "IdentityKind",
    "IncidentSeverity",
    "IncidentType",
    "OfferState",
    "RiskLevel",
    "RunStatus",
    "SecurityMode",
    "SovereigntyLevel",
    "ToolCallStatus",
    "WorkspaceType",
]

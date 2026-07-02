"""Sovereign Hermes kernel.

This subpackage contains deterministic governance and value-loop primitives for
Hermes. It complements the existing Hermes agents, registry, and orchestrator
without replacing them.
"""

from dealix.hermes.sovereign.models import (
    Asset,
    Decision,
    Execution,
    Opportunity,
    Outcome,
    Signal,
)
from dealix.hermes.sovereign.policy import (
    ActionRoute,
    PermissionDecision,
    SovereigntyLevel,
    TrustCheckResult,
    classify_action,
    permission_check,
    route_action,
    trust_check,
)
from dealix.hermes.sovereign.scoring import compute_money_score, compute_opportunity_score

__all__ = [
    "ActionRoute",
    "Asset",
    "Decision",
    "Execution",
    "Opportunity",
    "Outcome",
    "PermissionDecision",
    "Signal",
    "SovereigntyLevel",
    "TrustCheckResult",
    "classify_action",
    "compute_money_score",
    "compute_opportunity_score",
    "permission_check",
    "route_action",
    "trust_check",
]

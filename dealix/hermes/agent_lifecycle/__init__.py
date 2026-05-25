"""
Governed Agent Lifecycle.

Every agent moves through a fixed state machine:

    Proposed
    → Registered
    → Risk Scored
    → Tool Scoped
    → Context Scoped
    → Tested
    → Draft-Only
    → Approval-Gated
    → Limited Autonomy
    → Monitored
    → Improved / Restricted / Retired

Promotion between states is gated on measurable evidence — never on vibes.
"""

from __future__ import annotations

from dealix.hermes.agent_lifecycle.capability_scope import (
    CapabilityScope,
    ScopeViolation,
    validate_scope,
)
from dealix.hermes.agent_lifecycle.evaluation import (
    AgentEvaluation,
    PromotionCheck,
    evaluate_promotion_readiness,
)
from dealix.hermes.agent_lifecycle.promotion import (
    PromotionError,
    PromotionResult,
    promote,
)
from dealix.hermes.agent_lifecycle.registry import (
    AgentLifecycleStage,
    AgentRecord,
    AgentRegistry,
)
from dealix.hermes.agent_lifecycle.restriction import (
    RestrictionReason,
    restrict_agent,
)
from dealix.hermes.agent_lifecycle.retirement import retire_agent
from dealix.hermes.agent_lifecycle.risk_scoring import (
    AgentRiskScore,
    score_agent_risk,
)

__all__ = [
    "AgentLifecycleStage",
    "AgentRecord",
    "AgentRegistry",
    "AgentRiskScore",
    "score_agent_risk",
    "CapabilityScope",
    "ScopeViolation",
    "validate_scope",
    "AgentEvaluation",
    "PromotionCheck",
    "evaluate_promotion_readiness",
    "PromotionError",
    "PromotionResult",
    "promote",
    "RestrictionReason",
    "restrict_agent",
    "retire_agent",
]

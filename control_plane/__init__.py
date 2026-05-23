"""
Dealix Control Plane.

The control plane reads the current company state, produces the daily
CEO brief, routes decisions and approvals, runs the risk engine, scores
each system, and feeds the learning router.

Public symbols are exported from individual modules; this package init
is intentionally small to keep import surfaces predictable.
"""

from .company_state import CompanyState, snapshot
from .ceo_brief import CEOBrief, generate_ceo_brief
from .decision_engine import Decision, DecisionEngine
from .action_router import ActionRouter, RoutedAction
from .approval_router import ApprovalRouter, PendingApproval
from .risk_engine import RiskEngine, RiskItem
from .metrics_collector import MetricsCollector
from .system_scorecard import SystemScorecard, score_system
from .learning_router import LearningRouter, LearningSignal

__all__ = [
    "CompanyState",
    "snapshot",
    "CEOBrief",
    "generate_ceo_brief",
    "Decision",
    "DecisionEngine",
    "ActionRouter",
    "RoutedAction",
    "ApprovalRouter",
    "PendingApproval",
    "RiskEngine",
    "RiskItem",
    "MetricsCollector",
    "SystemScorecard",
    "score_system",
    "LearningRouter",
    "LearningSignal",
]

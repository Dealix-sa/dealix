"""
Dealix Autonomous Growth & Strategy Execution OS.

A draft-only, approval-first autonomous layer that plans and prepares
commercial work (proof packs, proposals, follow-up drafts, target lists,
content drafts) without a founder in the loop for the *thinking*, while
keeping the founder firmly in the loop for every *external* action.

Design constraints (non-negotiable):
- Draft-only: this package never sends WhatsApp/email/SMS/LinkedIn.
- Approval-first: any external or high-risk action is routed to an
  approval queue for founder decision — never auto-executed.
- Local-first: model routing prefers self-hosted (Ollama) with fallbacks.
- Auditable: every plan, action, and decision is appended to a proof log.
- Self-contained: depends only on the standard library + PyYAML, so it can
  run in a minimal CI/cron environment. It must not import agent or
  integration modules (see dealix/__init__.py contract).

Entry point: `orchestrator.AutonomousOS`.
"""

from __future__ import annotations

__version__ = "1.0.0"

from .safety_gate import SafetyGate, SafetyDecision  # noqa: F401
from .strategy_registry import Strategy, StrategyRegistry  # noqa: F401
from .execution_planner import ExecutionPlan, ExecutionPlanner, PlannedStep  # noqa: F401
from .action_queue import Action, ActionQueue  # noqa: F401
from .approval_queue import ApprovalItem, ApprovalQueue, ApprovalState  # noqa: F401
from .proof_logger import ProofLogger  # noqa: F401
from .learning_loop import LearningLoop  # noqa: F401
from .model_router import ModelChoice, ModelRouter  # noqa: F401
from .growth_engine import GrowthAction, GrowthEngine  # noqa: F401
from .orchestrator import AutonomousOS  # noqa: F401

__all__ = [
    "AutonomousOS",
    "SafetyGate",
    "SafetyDecision",
    "StrategyRegistry",
    "Strategy",
    "ExecutionPlanner",
    "ExecutionPlan",
    "PlannedStep",
    "ActionQueue",
    "Action",
    "ApprovalQueue",
    "ApprovalItem",
    "ApprovalState",
    "ProofLogger",
    "LearningLoop",
    "ModelRouter",
    "ModelChoice",
    "GrowthEngine",
    "GrowthAction",
]

"""Dealix autonomous strategy execution package.

Safe-by-default strategy execution primitives for draft-only internal operations.
"""

from .execution_planner import plan_daily_execution
from .safety_gate import SafetyDecision, evaluate_action_safety

__all__ = ["SafetyDecision", "evaluate_action_safety", "plan_daily_execution"]

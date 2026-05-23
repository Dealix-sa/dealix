"""
Action router.

Given a Decision, route it to (a) an internal workflow when its approval
class is `auto`, or (b) the approval queue when it requires founder
review. The router never sends external messages itself; it only routes.
"""
from __future__ import annotations

from dataclasses import dataclass

from .decision_engine import Decision


@dataclass(frozen=True, slots=True)
class RoutedAction:
    decision: Decision
    destination: str  # "workflow", "approval_queue", or "blocked"
    handler: str      # workflow id or queue key


class ActionRouter:
    """Pure-function router. No side effects; callers persist the result."""

    BLOCKED_ACTIONS = ("auto_send_external_outbound",)

    def route(self, decision: Decision) -> RoutedAction:
        label = decision.label.lower()
        if any(b in label for b in self.BLOCKED_ACTIONS):
            return RoutedAction(decision, "blocked", "blocked:doctrine")

        if decision.approval_class == "auto":
            handler = self._workflow_id_for(decision)
            return RoutedAction(decision, "workflow", handler)

        return RoutedAction(decision, "approval_queue", decision.approval_class)

    @staticmethod
    def _workflow_id_for(decision: Decision) -> str:
        label = decision.label.lower()
        if "lead" in label:
            return "dealix.workflows.daily_lead_discovery"
        if "review" in label:
            return "dealix.workflows.weekly_ceo_review"
        if "score" in label or "scoring" in label:
            return "dealix.workflows.lead_scoring_batch"
        return "dealix.workflows.daily_ceo_brief"

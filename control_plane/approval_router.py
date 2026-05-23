"""ApprovalRouter: route every action to A0 / A1 / A2 / A3.

A0 = automatic internal action.
A1 = review recommended (human edits AI draft).
A2 = explicit human approval required before external execution.
A3 = never auto-execute; founder-only.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict


class ApprovalLevel(str, Enum):
    A0 = "A0"
    A1 = "A1"
    A2 = "A2"
    A3 = "A3"


@dataclass
class RoutedAction:
    action: str
    level: ApprovalLevel
    reason: str


# Action → approval level mapping. Keep names lowercase, underscore-separated.
DEFAULT_ROUTES: Dict[str, ApprovalLevel] = {
    "lead_scoring": ApprovalLevel.A0,
    "crm_update": ApprovalLevel.A0,
    "lead_enrichment": ApprovalLevel.A0,
    "message_draft": ApprovalLevel.A1,
    "first_outbound": ApprovalLevel.A1,
    "followup_outbound": ApprovalLevel.A1,
    "proposal_draft": ApprovalLevel.A2,
    "proposal_send": ApprovalLevel.A2,
    "payment_terms_change": ApprovalLevel.A2,
    "public_content_publish": ApprovalLevel.A2,
    "public_compliance_claim": ApprovalLevel.A2,
    "contract_change": ApprovalLevel.A3,
    "nda_sign": ApprovalLevel.A3,
    "refund": ApprovalLevel.A3,
    "sensitive_data_export": ApprovalLevel.A3,
    "regulator_communication": ApprovalLevel.A3,
    "guaranteed_revenue_claim": ApprovalLevel.A3,
    "full_compliance_claim": ApprovalLevel.A3,
}


class ApprovalRouter:
    """Returns the required approval level for a named action."""

    def __init__(self, routes: Dict[str, ApprovalLevel] | None = None) -> None:
        self.routes = dict(DEFAULT_ROUTES)
        if routes:
            self.routes.update(routes)

    def route(self, action: str) -> RoutedAction:
        key = action.strip().lower()
        if key in self.routes:
            level = self.routes[key]
            return RoutedAction(
                action=action,
                level=level,
                reason=f"Mapped by policy to {level.value}.",
            )
        # Unknown actions are conservatively escalated to A2.
        return RoutedAction(
            action=action,
            level=ApprovalLevel.A2,
            reason="Unmapped action — default to A2 (explicit approval).",
        )

    def is_auto_executable(self, action: str) -> bool:
        return self.route(action).level == ApprovalLevel.A0

    def is_blocked_from_auto(self, action: str) -> bool:
        return self.route(action).level == ApprovalLevel.A3

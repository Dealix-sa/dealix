"""WhatsApp Client OS — metrics.

Deterministic aggregation over the JSONL stores. Counts only what is actually
recorded — no invented funnel numbers. Used by the founder ops surface and the
reports generator.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from auto_client_acquisition.governance_os import GovernanceDecision
from auto_client_acquisition.whatsapp_client_os import session_store as store
from auto_client_acquisition.whatsapp_client_os.schemas import ActionCardKind


def compute_metrics() -> dict[str, Any]:
    sessions = store.list_sessions()
    messages = store.list_messages()
    cards = store.list_cards()
    assessments = store.list_assessments()
    permissions = store.list_permissions()

    by_kind: Counter[str] = Counter(c.get("kind", "") for c in cards)
    by_intent: Counter[str] = Counter(m.intent for m in messages if m.direction == "inbound")

    return {
        "new_sessions": len(sessions),
        "inbound_messages": sum(1 for m in messages if m.direction == "inbound"),
        "completed_scans": len(assessments),
        "recommendations_generated": by_kind.get(ActionCardKind.RECOMMENDATION.value, 0),
        "action_cards": len(cards),
        "proposal_requests": by_kind.get(ActionCardKind.PROPOSAL.value, 0),
        "permission_cards": by_kind.get(ActionCardKind.PERMISSION.value, 0),
        "payment_handoffs": by_kind.get(ActionCardKind.PAYMENT_HANDOFF.value, 0),
        "support_tickets": by_kind.get(ActionCardKind.SUPPORT_ESCALATION.value, 0),
        "human_handoffs": sum(1 for s in sessions if s.handoff_open),
        "permissions_recorded": len(permissions),
        "by_card_kind": dict(by_kind),
        "by_intent": dict(by_intent),
        "governance_decision": GovernanceDecision.ALLOW.value,
    }


__all__ = ["compute_metrics"]

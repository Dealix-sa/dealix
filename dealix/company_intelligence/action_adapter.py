"""Fail-closed adapter from Revenue Graph NextBestAction to canonical Action.

Bridges ``auto_client_acquisition.revenue_graph.graph.NextBestAction``
into ``CanonicalAction`` without escalating authority. The operational
recommendation carries channel, rationale, and expected lift; this adapter
normalises it into the tenant-scoped, prioritized, queued shape the Company
Intelligence execution spine expects.

Key constraints:
  - Channel → ActionType mapping: whatsapp/email/linkedin → PREPARE_DRAFT,
    manual → INTERNAL_UPDATE.
  - External-effect actions (whatsapp, email, linkedin) always require
    approval and L4+ autonomy.
  - Manual-channel actions are internal-only (L2 autonomy).
  - Confidence from the recommendation maps to the action's confidence input.
  - ``expected_reply_lift`` maps to impact.
  - The adapter never grants execution authority.
"""
from __future__ import annotations

from typing import Any

from dealix.company_intelligence.action_contracts import (
    ActionType,
    AutonomyLevel,
    CanonicalAction,
    RiskLevel,
    build_action,
)

# ---------------------------------------------------------------------------
# Channel → action type mapping
# ---------------------------------------------------------------------------

_CHANNEL_ACTION_MAP: dict[str, ActionType] = {
    "whatsapp": ActionType.PREPARE_DRAFT,
    "email": ActionType.PREPARE_DRAFT,
    "linkedin": ActionType.PREPARE_DRAFT,
    "call": ActionType.SCHEDULE_MEETING,
    "meeting": ActionType.SCHEDULE_MEETING,
    "manual": ActionType.INTERNAL_UPDATE,
}

_EXTERNAL_CHANNELS = frozenset({"whatsapp", "email", "linkedin"})


def _resolve_action_type(channel: str) -> ActionType:
    """Map a recommendation channel to a canonical ActionType.

    Unknown channels fail-closed to ``INTERNAL_UPDATE``.
    """
    return _CHANNEL_ACTION_MAP.get(channel.lower().strip(), ActionType.INTERNAL_UPDATE)


def _is_external_channel(channel: str) -> bool:
    """Check whether a channel implies external communication."""
    return channel.lower().strip() in _EXTERNAL_CHANNELS


def _resolve_risk_level(channel: str, confidence: float) -> RiskLevel:
    """Derive risk level from channel and confidence.

    External channels carry higher risk; low confidence increases risk.
    """
    if _is_external_channel(channel):
        if confidence < 0.5:
            return RiskLevel.HIGH
        return RiskLevel.MEDIUM
    return RiskLevel.LOW


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def normalize_next_best_action(
    recommendation: Any,
    *,
    tenant_id: str,
    opportunity_id: str,
    department: str = "sales",
    company_id: str = "",
) -> CanonicalAction:
    """Normalize a ``NextBestAction`` into a ``CanonicalAction``.

    Parameters
    ----------
    recommendation:
        A ``NextBestAction`` or any duck-typed object with ``action``,
        ``channel``, ``rationale``, ``expected_reply_lift``, ``confidence``,
        and optionally ``playbook_id``.
    tenant_id:
        The tenant scope for the resulting canonical action.
    opportunity_id:
        The canonical opportunity_id this action belongs to.
    department:
        Department responsible (default: "sales").
    company_id:
        Company context for the action (used in idempotency key).
    """
    action_name = str(getattr(recommendation, "action", "") or "").strip()
    if not action_name:
        raise ValueError("recommendation must have a non-empty action")

    channel = str(getattr(recommendation, "channel", "manual") or "manual").strip()
    rationale = str(getattr(recommendation, "rationale", "") or "").strip()
    expected_lift = float(getattr(recommendation, "expected_reply_lift", 0.0) or 0.0)
    confidence = float(getattr(recommendation, "confidence", 0.5) or 0.5)
    playbook_id = str(getattr(recommendation, "playbook_id", "") or "").strip()

    # Clamp values
    confidence = _clamp(confidence)

    # Map channel to action type
    action_type = _resolve_action_type(channel)
    is_external = _is_external_channel(channel)
    risk_level = _resolve_risk_level(channel, confidence)

    # Playbook context enhances the idempotency key — the same action from
    # different playbooks should produce distinct canonical actions.

    # Autonomy level: external channels need L4+, manual is L2
    autonomy_level = (
        AutonomyLevel.L4_CONTROLLED_EXECUTE if is_external
        else AutonomyLevel.L2_DRAFT
    )

    # Impact from expected_reply_lift (normalized to 0–1 range)
    # Lift of 3.0+ → 1.0 impact, 0.0 → 0.1 (minimum)
    impact = _clamp(expected_lift / 3.0, low=0.1, high=1.0)

    # Urgency derived from confidence (higher confidence → higher urgency)
    urgency = _clamp(confidence * 0.8 + 0.2)

    # Reversibility: external actions are less reversible
    reversibility = 0.3 if is_external else 0.8

    # Effort: external actions require more effort (approval chain)
    effort = 0.6 if is_external else 0.3

    # Build idempotency key — includes playbook_id when present so the same
    # action recommended from different playbooks produces distinct entries.
    base_key = f"nba:{action_name}:{channel}:{company_id or opportunity_id}"
    idempotency_key = f"{base_key}:{playbook_id}" if playbook_id else base_key

    return build_action(
        tenant_id=tenant_id,
        idempotency_key=idempotency_key,
        action_type=action_type,
        department=department,
        risk_level=risk_level,
        autonomy_level=autonomy_level,
        opportunity_id=opportunity_id,
        trigger=f"next_best_action:{action_name}",
        objective=rationale,
        impact=impact,
        urgency=urgency,
        confidence=confidence,
        reversibility=reversibility,
        effort=effort,
        risk=max(0.01, 1.0 - confidence),
        approval_required=True,
        external_effect=is_external,
        proof_requirement="outcome_recorded" if is_external else "",
        expected_output=f"draft:{channel}" if is_external else "internal_update",
        failure_owner=department,
    )

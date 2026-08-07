"""Fail-closed adapter from operational learning events to canonical LearningEvent.

Bridges two operational sources into ``CanonicalLearningEvent`` without
escalating authority:

  1. ``auto_client_acquisition.learning_flywheel.aggregator.LearningEvent``
     — timestamped flywheel events from the execution loop.
  2. ``auto_client_acquisition.distribution_os.win_loss.WinLoss``
     — win/loss retrospective records with lessons and objections.

Key constraints:
  - The adapter never marks a learning event as ``applied`` (always False).
  - Approval is always required — the adapter does not grant policy authority.
  - Event kind → canonical LearningEventType via explicit mapping;
    unknown kinds fail-closed to ``TARGETING``.
  - Win/loss outcome affects confidence: won → 0.7, lost → 0.5,
    no_decision → 0.3 (hypothesis-level).
  - Win/loss ``lesson`` + ``next_change`` compose the recommended_change.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from dealix.company_intelligence.outcome_contracts import (
    CanonicalLearningEvent,
    LearningEventType,
    build_learning_event,
)

# ---------------------------------------------------------------------------
# LearningEvent kind → canonical type mapping
# ---------------------------------------------------------------------------

_KIND_MAP: dict[str, LearningEventType] = {
    # Targeting & scoring
    "signal_created": LearningEventType.TARGETING,
    "lead_created": LearningEventType.TARGETING,
    "lead_scored": LearningEventType.TARGETING,
    "churn_risk_detected": LearningEventType.TARGETING,
    # Data quality
    "decision_passport_created": LearningEventType.DATA_QUALITY,
    # Messaging
    "manual_message_sent": LearningEventType.MESSAGE,
    "reply_received": LearningEventType.MESSAGE,
    # Negotiation & actions
    "action_created": LearningEventType.NEGOTIATION,
    "action_approved": LearningEventType.NEGOTIATION,
    "action_rejected": LearningEventType.NEGOTIATION,
    # Offer
    "demo_booked": LearningEventType.OFFER,
    "pilot_requested": LearningEventType.OFFER,
    "upsell_offered": LearningEventType.OFFER,
    "upsell_accepted": LearningEventType.OFFER,
    # Delivery
    "diagnostic_delivered": LearningEventType.DELIVERY,
    "payment_confirmed": LearningEventType.DELIVERY,
    "delivery_started": LearningEventType.DELIVERY,
    "proof_created": LearningEventType.DELIVERY,
    "monthly_started": LearningEventType.DELIVERY,
    # Technical
    "feature_request_received": LearningEventType.TECHNICAL,
}


def _resolve_kind(kind: str) -> LearningEventType:
    """Map a flywheel event kind to a canonical LearningEventType.

    Unknown kinds fail-closed to ``TARGETING``.
    """
    return _KIND_MAP.get(kind.lower().strip(), LearningEventType.TARGETING)


# ---------------------------------------------------------------------------
# Win/loss outcome → confidence and type
# ---------------------------------------------------------------------------

_OUTCOME_CONFIDENCE: dict[str, float] = {
    "won": 0.7,
    "lost": 0.5,
    "no_decision": 0.3,
}

_OUTCOME_TYPE: dict[str, LearningEventType] = {
    "won": LearningEventType.NEGOTIATION,
    "lost": LearningEventType.NEGOTIATION,
    "no_decision": LearningEventType.TARGETING,
}


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


# ---------------------------------------------------------------------------
# Normalize flywheel LearningEvent
# ---------------------------------------------------------------------------


def normalize_learning_event(
    event: Any,
    *,
    tenant_id: str,
) -> CanonicalLearningEvent:
    """Normalize a flywheel ``LearningEvent`` into a ``CanonicalLearningEvent``.

    Parameters
    ----------
    event:
        A ``LearningEvent`` or any duck-typed object with ``kind``,
        ``customer_handle``, ``timestamp``, and optionally ``sector``,
        ``channel``, ``offer``, ``succeeded``, ``notes_en``, ``notes_ar``.
    tenant_id:
        The tenant scope for the resulting canonical learning event.
    """
    kind = str(getattr(event, "kind", "") or "").strip()
    if not kind:
        raise ValueError("event must have a non-empty kind")

    event_type = _resolve_kind(kind)

    # Parse timestamp
    timestamp_raw = getattr(event, "timestamp", None)
    if timestamp_raw is None:
        created_at = datetime.now(UTC)
    elif isinstance(timestamp_raw, datetime):
        created_at = timestamp_raw if timestamp_raw.tzinfo else timestamp_raw.replace(tzinfo=UTC)
    else:
        try:
            created_at = datetime.fromisoformat(str(timestamp_raw))
            if created_at.tzinfo is None:
                created_at = created_at.replace(tzinfo=UTC)
        except (ValueError, TypeError):
            created_at = datetime.now(UTC)

    # Build evidence refs from context fields
    customer_handle = str(getattr(event, "customer_handle", "") or "").strip()
    sector = str(getattr(event, "sector", "") or "").strip()
    channel = str(getattr(event, "channel", "") or "").strip()
    offer = str(getattr(event, "offer", "") or "").strip()

    refs: list[str] = [f"flywheel:{kind}"]
    if customer_handle:
        refs.append(f"customer:{customer_handle}")
    if sector:
        refs.append(f"sector:{sector}")
    if channel:
        refs.append(f"channel:{channel}")
    if offer:
        refs.append(f"offer:{offer}")

    # Succeeded flag affects confidence
    succeeded = getattr(event, "succeeded", None)
    if succeeded is True:
        confidence = 0.7
    elif succeeded is False:
        confidence = 0.4
    else:
        confidence = 0.5

    # Recommended change from notes
    notes_en = str(getattr(event, "notes_en", "") or "").strip()
    notes_ar = str(getattr(event, "notes_ar", "") or "").strip()
    recommended_change = notes_en or notes_ar or f"Review {kind} event for {customer_handle or 'unknown'}"

    return build_learning_event(
        tenant_id=tenant_id,
        event_type=event_type,
        evidence_refs=refs,
        confidence=confidence,
        recommended_change=recommended_change,
        created_at=created_at,
        hypothesis_only=True,
    )


# ---------------------------------------------------------------------------
# Normalize win/loss record
# ---------------------------------------------------------------------------


def normalize_win_loss(
    record: Any,
    *,
    tenant_id: str,
) -> CanonicalLearningEvent:
    """Normalize a ``WinLoss`` record into a ``CanonicalLearningEvent``.

    Parameters
    ----------
    record:
        A ``WinLoss`` or any duck-typed object with ``outcome``, ``company``,
        ``lesson``, ``next_change``, and optionally ``sector``, ``channel``,
        ``offer``, ``reason``, ``objection``.
    tenant_id:
        The tenant scope for the resulting canonical learning event.
    """
    outcome = str(getattr(record, "outcome", "no_decision") or "no_decision").strip().lower()
    lesson = str(getattr(record, "lesson", "") or "").strip()
    next_change = str(getattr(record, "next_change", "") or "").strip()
    company = str(getattr(record, "company", "") or "").strip()

    if not lesson and not next_change:
        raise ValueError("win/loss record must have a non-empty lesson or next_change")

    # Event type and confidence from outcome
    event_type = _OUTCOME_TYPE.get(outcome, LearningEventType.TARGETING)
    confidence = _clamp(_OUTCOME_CONFIDENCE.get(outcome, 0.3))

    # Build evidence refs
    refs: list[str] = [f"win_loss:{outcome}"]
    if company:
        refs.append(f"company:{company}")

    sector = str(getattr(record, "sector", "") or "").strip()
    channel = str(getattr(record, "channel", "") or "").strip()
    offer = str(getattr(record, "offer", "") or "").strip()
    reason = str(getattr(record, "reason", "") or "").strip()
    objection = str(getattr(record, "objection", "") or "").strip()

    if sector:
        refs.append(f"sector:{sector}")
    if channel:
        refs.append(f"channel:{channel}")
    if offer:
        refs.append(f"offer:{offer}")
    if reason:
        refs.append(f"reason:{reason}")
    if objection:
        refs.append(f"objection:{objection}")

    # Recommended change from lesson + next_change
    parts: list[str] = []
    if lesson:
        parts.append(lesson)
    if next_change:
        parts.append(f"Next: {next_change}")
    recommended_change = " | ".join(parts)

    # Parse created_at
    created_at_raw = getattr(record, "created_at", None)
    if created_at_raw is None:
        created_at = datetime.now(UTC)
    elif isinstance(created_at_raw, datetime):
        created_at = created_at_raw if created_at_raw.tzinfo else created_at_raw.replace(tzinfo=UTC)
    else:
        try:
            created_at = datetime.fromisoformat(str(created_at_raw))
            if created_at.tzinfo is None:
                created_at = created_at.replace(tzinfo=UTC)
        except (ValueError, TypeError):
            created_at = datetime.now(UTC)

    return build_learning_event(
        tenant_id=tenant_id,
        event_type=event_type,
        evidence_refs=refs,
        confidence=confidence,
        recommended_change=recommended_change,
        created_at=created_at,
        hypothesis_only=True,
    )

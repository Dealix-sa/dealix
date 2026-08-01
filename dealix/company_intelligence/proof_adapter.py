"""Fail-closed adapter from the existing proof ledger into canonical proof truth."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.proof_ledger.schemas import ProofEventType
from dealix.company_intelligence.outcome_contracts import (
    CanonicalProofEvent,
    ProofSourceEventType,
    ProofType,
    build_proof_event,
)

_RECOGNITION_EVENT_TYPES: dict[ProofType, frozenset[str]] = {
    ProofType.PAYMENT_EVIDENCE: frozenset({ProofEventType.PAYMENT_CONFIRMED.value}),
    ProofType.DELIVERY_EVIDENCE: frozenset(
        {ProofEventType.DELIVERY_TASK_COMPLETED.value}
    ),
}
_SYNTHETIC_MARKERS = ("synthetic", "fixture", "demo")


def _event_type_value(record: Any) -> str:
    value = getattr(record, "event_type", "")
    return str(getattr(value, "value", value)).strip()


def _is_synthetic_record(record: Any) -> bool:
    payload = getattr(record, "payload", {})
    if isinstance(payload, dict) and (
        payload.get("is_synthetic") is True or payload.get("synthetic") is True
    ):
        return True

    evidence_source = str(getattr(record, "evidence_source", "")).lower()
    return any(marker in evidence_source for marker in _SYNTHETIC_MARKERS)


def normalize_proof_event(
    record: Any,
    *,
    tenant_id: str,
    entity_type: str,
    entity_id: str,
    proof_type: ProofType,
    verifier: str,
    source_outcome_id: str | None = None,
) -> CanonicalProofEvent:
    """Adapt ledger proof while preventing caller-selected revenue/delivery truth.

    Revenue and completed-delivery evidence must originate from their matching
    ledger event types. Generic outcome evidence remains available for other
    ledger events, while technical verification requires a dedicated canonical
    source rather than being inferred from the commercial ledger.
    """

    evidence_source = str(getattr(record, "evidence_source", "")).strip()
    if not evidence_source:
        raise ValueError("proof-ledger record requires evidence_source")

    if proof_type == ProofType.TECHNICAL_VERIFICATION:
        raise ValueError(
            "technical verification cannot be inferred from the commercial proof ledger"
        )

    allowed_events = _RECOGNITION_EVENT_TYPES.get(proof_type)
    if allowed_events is not None:
        event_type = _event_type_value(record)
        if event_type not in allowed_events:
            raise ValueError(
                f"{proof_type.value} requires matching proof-ledger event type"
            )
        if _is_synthetic_record(record):
            raise ValueError("synthetic payment or delivery proof is forbidden")

    return build_proof_event(
        tenant_id=tenant_id,
        entity_type=entity_type,
        entity_id=entity_id,
        proof_type=proof_type,
        evidence_ref=evidence_source,
        source_event_type=(
            ProofSourceEventType.PAYMENT_CONFIRMED
            if proof_type == ProofType.PAYMENT_EVIDENCE
            else ProofSourceEventType.DELIVERY_TASK_COMPLETED
            if proof_type == ProofType.DELIVERY_EVIDENCE
            else None
        ),
        verified_at=record.created_at,
        verifier=verifier,
        source_outcome_id=source_outcome_id,
        confidence=record.confidence,
        is_synthetic=False,
        publication_approved=record.is_publishable(),
    )

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

_SOURCE_EVENT_TYPES: dict[ProofType, ProofSourceEventType] = {
    ProofType.PAYMENT_EVIDENCE: ProofSourceEventType.PAYMENT_CONFIRMED,
    ProofType.DELIVERY_EVIDENCE: ProofSourceEventType.DELIVERY_TASK_COMPLETED,
}

_SYNTHETIC_PREFIXES = ("synthetic:", "synthetic://", "fixture:", "demo:")


def _event_value(record: Any) -> str:
    value = getattr(record, "event_type", "")
    if hasattr(value, "value"):
        value = value.value
    return str(value).strip()


def _payload(record: Any) -> dict[str, Any]:
    value = getattr(record, "payload", {})
    return value if isinstance(value, dict) else {}


def _is_synthetic_record(record: Any) -> bool:
    evidence_source = str(getattr(record, "evidence_source", "")).strip().lower()
    payload = _payload(record)
    return (
        bool(payload.get("is_synthetic"))
        or bool(payload.get("synthetic"))
        or evidence_source.startswith(_SYNTHETIC_PREFIXES)
    )


def _publication_approved(record: Any, *, is_synthetic: bool) -> bool:
    if is_synthetic:
        return False
    check = getattr(record, "is_publishable", None)
    return bool(check()) if callable(check) else False


def normalize_proof_event(
    record: Any,
    *,
    tenant_id: str,
    entity_type: str,
    entity_id: str,
    proof_type: ProofType,
    verifier: str,
) -> CanonicalProofEvent:
    """Normalize one legacy ledger record without escalating its authority.

    Payment and delivery truth require exact matching ledger event types and
    reject all synthetic provenance. Generic outcome evidence preserves its
    synthetic state and can never become publication-approved when synthetic.
    Commercial ledger records cannot establish technical verification.
    """

    event_value = _event_value(record)
    evidence_ref = str(getattr(record, "evidence_source", "")).strip()
    if not evidence_ref:
        raise ValueError("proof ledger evidence_source is required")

    if proof_type == ProofType.TECHNICAL_VERIFICATION:
        raise ValueError("technical verification cannot be inferred from commercial ledger")

    allowed_events = _RECOGNITION_EVENT_TYPES.get(proof_type)
    if allowed_events is not None and event_value not in allowed_events:
        raise ValueError(
            f"{proof_type.value} requires matching proof-ledger event type"
        )

    is_synthetic = _is_synthetic_record(record)
    if is_synthetic and proof_type in {
        ProofType.PAYMENT_EVIDENCE,
        ProofType.DELIVERY_EVIDENCE,
    }:
        raise ValueError("synthetic payment or delivery proof is forbidden")

    payload = _payload(record)
    source_outcome_id_raw = payload.get("source_outcome_id")
    source_outcome_id = (
        source_outcome_id_raw.strip()
        if isinstance(source_outcome_id_raw, str) and source_outcome_id_raw.strip()
        else None
    )

    confidence_raw = getattr(record, "confidence", 1.0)
    confidence = float(confidence_raw)

    return build_proof_event(
        tenant_id=tenant_id,
        entity_type=entity_type,
        entity_id=entity_id,
        proof_type=proof_type,
        evidence_ref=evidence_ref,
        source_event_type=_SOURCE_EVENT_TYPES.get(proof_type),
        source_outcome_id=source_outcome_id,
        verified_at=record.created_at,
        verifier=verifier,
        confidence=confidence,
        is_synthetic=is_synthetic,
        publication_approved=_publication_approved(
            record, is_synthetic=is_synthetic
        ),
    )

from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from auto_client_acquisition.proof_ledger.schemas import ProofEventType
from dealix.company_intelligence.outcome_contracts import (
    ProofType,
    normalize_proof_event,
)

NOW = datetime(2026, 8, 1, 12, 0, tzinfo=UTC)


def _record(
    event_type: ProofEventType,
    *,
    evidence_source: str = "artifact:verified-1",
    payload: dict[str, object] | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        event_type=event_type,
        evidence_source=evidence_source,
        payload=payload or {},
        created_at=NOW,
        confidence=1.0,
        is_publishable=lambda: False,
    )


def _normalize(record: SimpleNamespace, proof_type: ProofType):
    return normalize_proof_event(
        record,
        tenant_id="tenant-a",
        entity_type="engagement",
        entity_id="eng-1",
        proof_type=proof_type,
        verifier="operator-a",
    )


def test_invoice_prepared_cannot_escalate_to_payment_evidence() -> None:
    with pytest.raises(ValueError, match="matching proof-ledger event type"):
        _normalize(
            _record(ProofEventType.INVOICE_PREPARED),
            ProofType.PAYMENT_EVIDENCE,
        )


def test_only_payment_confirmed_can_become_payment_evidence() -> None:
    proof = _normalize(
        _record(
            ProofEventType.PAYMENT_CONFIRMED,
            evidence_source="bank:receipt-1",
        ),
        ProofType.PAYMENT_EVIDENCE,
    )

    assert proof.proof_type == ProofType.PAYMENT_EVIDENCE
    assert proof.evidence_ref == "bank:receipt-1"


def test_delivery_started_cannot_escalate_to_completed_delivery() -> None:
    with pytest.raises(ValueError, match="matching proof-ledger event type"):
        _normalize(
            _record(ProofEventType.DELIVERY_STARTED),
            ProofType.DELIVERY_EVIDENCE,
        )


def test_only_completed_task_can_become_delivery_evidence() -> None:
    proof = _normalize(
        _record(ProofEventType.DELIVERY_TASK_COMPLETED),
        ProofType.DELIVERY_EVIDENCE,
    )

    assert proof.proof_type == ProofType.DELIVERY_EVIDENCE


@pytest.mark.parametrize(
    ("evidence_source", "payload"),
    [
        ("synthetic:payment", {}),
        ("fixture:delivery", {}),
        ("artifact:payment", {"is_synthetic": True}),
    ],
)
def test_synthetic_recognition_records_are_rejected(
    evidence_source: str,
    payload: dict[str, object],
) -> None:
    with pytest.raises(ValueError, match="synthetic payment or delivery"):
        _normalize(
            _record(
                ProofEventType.PAYMENT_CONFIRMED,
                evidence_source=evidence_source,
                payload=payload,
            ),
            ProofType.PAYMENT_EVIDENCE,
        )


def test_commercial_ledger_cannot_claim_technical_verification() -> None:
    with pytest.raises(ValueError, match="technical verification cannot be inferred"):
        _normalize(
            _record(ProofEventType.RISK_BLOCKED),
            ProofType.TECHNICAL_VERIFICATION,
        )

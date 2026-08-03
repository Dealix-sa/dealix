from __future__ import annotations

from datetime import UTC, date, datetime
from types import SimpleNamespace

import pytest

from auto_client_acquisition.proof_ledger.schemas import ProofEventType
from dealix.company_intelligence.outcome_contracts import (
    OutcomeEventType,
    ProofSourceEventType,
    ProofType,
    build_daily_command,
    build_proof_event,
)
from dealix.company_intelligence.proof_adapter import normalize_proof_event
from scripts.commercial.run_company_loop_simulation import run_loop

NOW = datetime(2026, 8, 3, 5, 0, tzinfo=UTC)


def test_mutated_outcome_proof_cannot_be_laundered_into_revenue() -> None:
    outcome_proof = build_proof_event(
        tenant_id="tenant-a",
        entity_type="opportunity",
        entity_id="opp-1",
        proof_type=ProofType.OUTCOME_EVIDENCE,
        evidence_ref="crm:reply-1",
        verified_at=NOW,
        verifier="operator-a",
    )
    forged = outcome_proof.model_copy(
        update={
            "proof_type": ProofType.PAYMENT_EVIDENCE,
            "source_event_type": ProofSourceEventType.PAYMENT_CONFIRMED,
        }
    )

    with pytest.raises(ValueError, match="proof_id does not match"):
        build_daily_command(
            tenant_id="tenant-a",
            command_date=date(2026, 8, 3),
            priorities=[],
            approval_items=[],
            proofs=[forged],
            learning_events=[],
            generated_at=NOW,
        )


def test_generic_synthetic_ledger_proof_preserves_provenance() -> None:
    record = SimpleNamespace(
        event_type=OutcomeEventType.PROSPECT_REPLIED.value,
        evidence_source="synthetic://fixture/reply-1",
        payload={"is_synthetic": True},
        created_at=NOW,
        confidence=0.8,
        is_publishable=lambda: True,
    )

    proof = normalize_proof_event(
        record,
        tenant_id="tenant-a",
        entity_type="opportunity",
        entity_id="opp-1",
        proof_type=ProofType.OUTCOME_EVIDENCE,
        verifier="test-suite",
    )

    assert proof.is_synthetic is True
    assert proof.publication_approved is False


def test_legacy_synthetic_payload_cannot_be_laundered_into_payment() -> None:
    record = SimpleNamespace(
        event_type=ProofEventType.PAYMENT_CONFIRMED.value,
        evidence_source="legacy-ledger:payment-1",
        payload={"synthetic": True},
        created_at=NOW,
        confidence=1.0,
        is_publishable=lambda: True,
    )

    with pytest.raises(ValueError, match="synthetic payment or delivery proof is forbidden"):
        normalize_proof_event(
            record,
            tenant_id="tenant-a",
            entity_type="opportunity",
            entity_id="opp-1",
            proof_type=ProofType.PAYMENT_EVIDENCE,
            verifier="test-suite",
        )


def test_legacy_synthetic_payload_cannot_be_laundered_into_delivery() -> None:
    record = SimpleNamespace(
        event_type=ProofEventType.DELIVERY_TASK_COMPLETED.value,
        evidence_source="legacy-ledger:delivery-1",
        payload={"synthetic": True},
        created_at=NOW,
        confidence=1.0,
        is_publishable=lambda: True,
    )

    with pytest.raises(ValueError, match="synthetic payment or delivery proof is forbidden"):
        normalize_proof_event(
            record,
            tenant_id="tenant-a",
            entity_type="delivery",
            entity_id="delivery-1",
            proof_type=ProofType.DELIVERY_EVIDENCE,
            verifier="test-suite",
        )


def test_draft_only_loop_remains_explicitly_synthetic() -> None:
    result = run_loop("lead_to_cash", mode="draft_only")

    assert result["status"] == "blocked_pending_approval"
    assert result["is_synthetic"] is True
    assert result["external_actions_executed"] == 0
    assert all(event["is_synthetic"] is True for event in result["outcome_events"])
    assert all(proof["is_synthetic"] is True for proof in result["proof_events"])
    assert all(approval["is_synthetic"] is True for approval in result["approvals"])

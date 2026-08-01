from __future__ import annotations

from datetime import UTC, date, datetime
from types import SimpleNamespace

import pytest

from dealix.company_intelligence.outcome_contracts import (
    CanonicalDailyCommand,
    EvidenceState,
    LearningEventType,
    OutcomeEventType,
    ProofSourceEventType,
    ProofType,
    build_daily_command,
    build_learning_event,
    build_outcome_event,
    build_proof_event,
    normalize_proof_event,
)

NOW = datetime(2026, 7, 31, 12, 0, tzinfo=UTC)


def test_outcome_is_deterministic_and_requires_sorted_evidence() -> None:
    first = build_outcome_event(
        tenant_id="tenant-a",
        action_id="action-1",
        event_type=OutcomeEventType.PROSPECT_REPLIED,
        occurred_at=NOW,
        evidence_refs=["gmail:thread-1", "approval:1", "gmail:thread-1"],
    )
    second = build_outcome_event(
        tenant_id="tenant-a",
        action_id="action-1",
        event_type=OutcomeEventType.PROSPECT_REPLIED,
        occurred_at=NOW,
        evidence_refs=["approval:1", "gmail:thread-1"],
    )

    assert first.outcome_id == second.outcome_id
    assert first.evidence_refs == ["approval:1", "gmail:thread-1"]


def test_synthetic_payment_and_delivery_outcomes_are_forbidden() -> None:
    for event_type in (
        OutcomeEventType.PAYMENT_RECEIVED,
        OutcomeEventType.DELIVERY_COMPLETED,
    ):
        with pytest.raises(ValueError, match="synthetic financial or delivery"):
            build_outcome_event(
                tenant_id="tenant-a",
                action_id="action-1",
                event_type=event_type,
                occurred_at=NOW,
                evidence_refs=["synthetic:fixture"],
                is_synthetic=True,
            )


def test_payment_and_delivery_proof_cannot_be_synthetic() -> None:
    for proof_type in (ProofType.PAYMENT_EVIDENCE, ProofType.DELIVERY_EVIDENCE):
        with pytest.raises(ValueError, match="synthetic payment or delivery proof"):
            build_proof_event(
                tenant_id="tenant-a",
                entity_type="opportunity",
                entity_id="opp-1",
                proof_type=proof_type,
                evidence_ref="synthetic:fixture",
                source_event_type=(
                    ProofSourceEventType.PAYMENT_CONFIRMED
                    if proof_type == ProofType.PAYMENT_EVIDENCE
                    else ProofSourceEventType.DELIVERY_TASK_COMPLETED
                ),
                verified_at=NOW,
                verifier="test-suite",
                is_synthetic=True,
            )


def test_existing_proof_ledger_adapter_requires_real_evidence_source() -> None:
    empty_record = SimpleNamespace(
        evidence_source="",
        created_at=NOW,
        confidence=1.0,
        is_publishable=lambda: False,
    )
    with pytest.raises(ValueError, match="evidence_source"):
        normalize_proof_event(
            empty_record,
            tenant_id="tenant-a",
            entity_type="opportunity",
            entity_id="opp-1",
            proof_type=ProofType.OUTCOME_EVIDENCE,
            verifier="test-suite",
        )

    record = SimpleNamespace(
        evidence_source="artifact:proof-1",
        created_at=NOW,
        confidence=0.9,
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
    assert proof.evidence_ref == "artifact:proof-1"
    assert proof.publication_approved is True


def test_learning_is_evidence_bounded_and_never_auto_applies() -> None:
    learning = build_learning_event(
        tenant_id="tenant-a",
        event_type=LearningEventType.MESSAGE,
        evidence_refs=["outcome:1", "draft:1"],
        confidence=0.4,
        recommended_change="Test a shorter CTA",
        created_at=NOW,
    )

    assert learning.hypothesis_only is True
    assert learning.approval_required is True
    assert learning.applied is False
    assert learning.official_policy_change_allowed is False


def test_daily_command_never_recognizes_revenue_without_payment_proof() -> None:
    learning = build_learning_event(
        tenant_id="tenant-a",
        event_type=LearningEventType.TARGETING,
        evidence_refs=["outcome:1"],
        confidence=0.5,
        recommended_change="Review the target segment",
        created_at=NOW,
    )
    outcome_proof = build_proof_event(
        tenant_id="tenant-a",
        entity_type="opportunity",
        entity_id="opp-1",
        proof_type=ProofType.OUTCOME_EVIDENCE,
        evidence_ref="crm:reply-1",
        verified_at=NOW,
        verifier="operator-a",
    )

    command = build_daily_command(
        tenant_id="tenant-a",
        command_date=date(2026, 7, 31),
        priorities=["prepare discovery"],
        approval_items=["approve email draft"],
        proofs=[outcome_proof],
        learning_events=[learning],
        generated_at=NOW,
    )

    assert command.revenue_state == EvidenceState.NOT_EVIDENCED
    assert command.recognized_revenue is False
    assert command.payment_proof_ids == []
    assert command.delivery_state == EvidenceState.NOT_EVIDENCED
    assert command.delivery_completed is False
    assert command.delivery_proof_ids == []


def test_daily_command_recognizes_only_payment_and_delivery_proof() -> None:
    payment = build_proof_event(
        tenant_id="tenant-a",
        entity_type="opportunity",
        entity_id="opp-1",
        proof_type=ProofType.PAYMENT_EVIDENCE,
        evidence_ref="bank:receipt-1",
        source_event_type=ProofSourceEventType.PAYMENT_CONFIRMED,
        verified_at=NOW,
        verifier="operator-a",
    )
    delivery = build_proof_event(
        tenant_id="tenant-a",
        entity_type="engagement",
        entity_id="eng-1",
        proof_type=ProofType.DELIVERY_EVIDENCE,
        evidence_ref="artifact:proof-pack-1",
        source_event_type=ProofSourceEventType.DELIVERY_TASK_COMPLETED,
        verified_at=NOW,
        verifier="operator-a",
    )

    first = build_daily_command(
        tenant_id="tenant-a",
        command_date=date(2026, 7, 31),
        priorities=["renewal review", "renewal review"],
        approval_items=[],
        proofs=[delivery, payment],
        learning_events=[],
        generated_at=NOW,
    )
    second = build_daily_command(
        tenant_id="tenant-a",
        command_date=date(2026, 7, 31),
        priorities=["renewal review"],
        approval_items=[],
        proofs=[payment, delivery],
        learning_events=[],
        generated_at=datetime(2026, 7, 31, 13, 0, tzinfo=UTC),
    )

    assert first.command_id == second.command_id
    assert first.revenue_state == EvidenceState.PAYMENT_EVIDENCED
    assert first.recognized_revenue is True
    assert first.payment_proof_ids == [payment.proof_id]
    assert first.delivery_state == EvidenceState.DELIVERY_EVIDENCED
    assert first.delivery_completed is True
    assert first.delivery_proof_ids == [delivery.proof_id]


def test_direct_financial_and_delivery_proofs_require_matching_source_events() -> None:
    with pytest.raises(ValueError, match="requires source event payment_confirmed"):
        build_proof_event(
            tenant_id="tenant-a",
            entity_type="opportunity",
            entity_id="opp-1",
            proof_type=ProofType.PAYMENT_EVIDENCE,
            evidence_ref="bank:receipt-1",
            verified_at=NOW,
            verifier="operator-a",
        )

    with pytest.raises(
        ValueError, match="requires source event delivery_task_completed"
    ):
        build_proof_event(
            tenant_id="tenant-a",
            entity_type="engagement",
            entity_id="eng-1",
            proof_type=ProofType.DELIVERY_EVIDENCE,
            evidence_ref="artifact:proof-pack-1",
            verified_at=NOW,
            verifier="operator-a",
            source_event_type=ProofSourceEventType.PAYMENT_CONFIRMED,
        )


def test_direct_command_rejects_untyped_proof_reference() -> None:
    with pytest.raises(ValueError, match="typed proof objects"):
        CanonicalDailyCommand(
            tenant_id="tenant-a",
            command_id="forged-command",
            command_date=date(2026, 7, 31),
            priorities=[],
            approval_items=[],
            proofs=[],
            proof_ids=["proof_fabricated"],
            payment_proof_ids=["proof_fabricated"],
            delivery_proof_ids=[],
            learning_ids=[],
            revenue_state=EvidenceState.PAYMENT_EVIDENCED,
            delivery_state=EvidenceState.NOT_EVIDENCED,
            recognized_revenue=True,
            delivery_completed=False,
            generated_at=NOW,
        )


def test_direct_command_rejects_outcome_proof_laundered_as_payment() -> None:
    outcome_proof = build_proof_event(
        tenant_id="tenant-a",
        entity_type="opportunity",
        entity_id="opp-1",
        proof_type=ProofType.OUTCOME_EVIDENCE,
        evidence_ref="crm:reply-1",
        verified_at=NOW,
        verifier="operator-a",
    )
    with pytest.raises(ValueError, match="typed payment proofs"):
        CanonicalDailyCommand(
            tenant_id="tenant-a",
            command_id="forged-command",
            command_date=date(2026, 7, 31),
            priorities=[],
            approval_items=[],
            proofs=[outcome_proof],
            proof_ids=[outcome_proof.proof_id],
            payment_proof_ids=[outcome_proof.proof_id],
            delivery_proof_ids=[],
            learning_ids=[],
            revenue_state=EvidenceState.PAYMENT_EVIDENCED,
            delivery_state=EvidenceState.NOT_EVIDENCED,
            recognized_revenue=True,
            delivery_completed=False,
            generated_at=NOW,
        )


def test_direct_command_cannot_claim_revenue_without_referenced_payment_proof() -> None:
    with pytest.raises(
        ValueError,
        match="recognized revenue requires referenced payment proof",
    ):
        CanonicalDailyCommand(
            tenant_id="tenant-a",
            command_id="forged-command",
            command_date=date(2026, 7, 31),
            priorities=[],
            approval_items=[],
            proof_ids=[],
            payment_proof_ids=[],
            delivery_proof_ids=[],
            learning_ids=[],
            revenue_state=EvidenceState.PAYMENT_EVIDENCED,
            delivery_state=EvidenceState.NOT_EVIDENCED,
            recognized_revenue=True,
            delivery_completed=False,
            generated_at=NOW,
        )


def test_typed_proof_ids_must_exist_in_command_proof_ids() -> None:
    with pytest.raises(ValueError, match="payment_proof_ids must be included"):
        CanonicalDailyCommand(
            tenant_id="tenant-a",
            command_id="forged-command",
            command_date=date(2026, 7, 31),
            priorities=[],
            approval_items=[],
            proof_ids=[],
            payment_proof_ids=["proof-payment-1"],
            delivery_proof_ids=[],
            learning_ids=[],
            revenue_state=EvidenceState.PAYMENT_EVIDENCED,
            delivery_state=EvidenceState.NOT_EVIDENCED,
            recognized_revenue=True,
            delivery_completed=False,
            generated_at=NOW,
        )


def test_daily_command_rejects_cross_tenant_evidence() -> None:
    proof = build_proof_event(
        tenant_id="tenant-b",
        entity_type="opportunity",
        entity_id="opp-2",
        proof_type=ProofType.OUTCOME_EVIDENCE,
        evidence_ref="crm:reply-2",
        verified_at=NOW,
        verifier="operator-b",
    )

    with pytest.raises(ValueError, match="cross-tenant proof"):
        build_daily_command(
            tenant_id="tenant-a",
            command_date=date(2026, 7, 31),
            priorities=[],
            approval_items=[],
            proofs=[proof],
            learning_events=[],
            generated_at=NOW,
        )

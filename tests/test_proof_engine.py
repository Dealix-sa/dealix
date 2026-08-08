"""Tests for the Proof & Outcome Validation Engine.

Covers outcome validation, proof pack assembly, evidence assessment,
proof completeness, and safety invariants.
"""
from __future__ import annotations

from datetime import UTC, datetime

import pytest

from dealix.company_intelligence.outcome_contracts import (
    EvidenceState,
    OutcomeEventType,
    ProofSourceEventType,
    ProofType,
    build_outcome_event,
    build_proof_event,
)
from dealix.company_intelligence.proof_engine import (
    EvidenceAssessment,
    EvidenceStrength,
    OutcomeValidation,
    ProofCompleteness,
    ProofCompletionStatus,
    ProofPack,
    ValidationResult,
    assess_evidence_strength,
    build_proof_pack,
    check_proof_completeness,
    validate_outcome,
)

TENANT = "tenant_test_proof"
SOURCE = "test_source"
NOW = datetime.now(UTC)


def _make_outcome(**overrides):
    defaults = {
        "tenant_id": TENANT,
        "action_id": "action_001",
        "event_type": OutcomeEventType.MEETING_BOOKED,
        "occurred_at": NOW,
        "evidence_refs": ["ref_001"],
    }
    defaults.update(overrides)
    return build_outcome_event(**defaults)


def _make_proof(**overrides):
    defaults = {
        "tenant_id": TENANT,
        "entity_type": "opportunity",
        "entity_id": "opp_001",
        "proof_type": ProofType.OUTCOME_EVIDENCE,
        "evidence_ref": "evidence_001",
        "verified_at": NOW,
        "verifier": "system",
    }
    defaults.update(overrides)
    return build_proof_event(**defaults)


# -----------------------------------------------------------------------
# Outcome validation
# -----------------------------------------------------------------------


class TestOutcomeValidation:
    def test_valid_outcome(self):
        outcome = _make_outcome()
        validation = validate_outcome(outcome, source_id=SOURCE)
        assert isinstance(validation, OutcomeValidation)
        assert validation.result == ValidationResult.VALID
        assert validation.evidence_strength == EvidenceStrength.MODERATE

    def test_deterministic_id(self):
        outcome = _make_outcome()
        v1 = validate_outcome(outcome, source_id=SOURCE)
        v2 = validate_outcome(outcome, source_id=SOURCE)
        assert v1.validation_id == v2.validation_id
        assert v1.validation_id.startswith("validation_")

    def test_multiple_evidence_strong(self):
        outcome = _make_outcome(
            evidence_refs=["ref_a", "ref_b"],
        )
        validation = validate_outcome(outcome, source_id=SOURCE)
        assert validation.evidence_strength == EvidenceStrength.STRONG

    def test_three_plus_evidence_conclusive(self):
        outcome = _make_outcome(
            evidence_refs=["ref_a", "ref_b", "ref_c"],
        )
        validation = validate_outcome(outcome, source_id=SOURCE)
        assert validation.evidence_strength == EvidenceStrength.CONCLUSIVE

    def test_low_confidence_insufficient(self):
        outcome = _make_outcome(confidence=0.3)
        validation = validate_outcome(outcome, source_id=SOURCE)
        assert validation.result == ValidationResult.INSUFFICIENT_EVIDENCE
        assert validation.evidence_strength == EvidenceStrength.WEAK

    def test_synthetic_outcome_weak(self):
        outcome = _make_outcome(
            event_type=OutcomeEventType.PROSPECT_REPLIED,
            is_synthetic=True,
        )
        validation = validate_outcome(outcome, source_id=SOURCE)
        assert validation.result == ValidationResult.VALID
        assert validation.evidence_strength == EvidenceStrength.WEAK
        assert "synthetic" in validation.issues[0]


# -----------------------------------------------------------------------
# Proof pack assembly
# -----------------------------------------------------------------------


class TestProofPack:
    def test_empty_pack(self):
        pack = build_proof_pack(
            tenant_id=TENANT,
            entity_type="opportunity",
            entity_id="opp_001",
            source_id=SOURCE,
        )
        assert isinstance(pack, ProofPack)
        assert pack.proof_count == 0
        assert pack.completeness == ProofCompletionStatus.MISSING
        assert pack.revenue_state == EvidenceState.NOT_EVIDENCED

    def test_deterministic_id(self):
        p1 = build_proof_pack(
            tenant_id=TENANT,
            entity_type="opportunity",
            entity_id="opp_001",
            source_id=SOURCE,
        )
        p2 = build_proof_pack(
            tenant_id=TENANT,
            entity_type="opportunity",
            entity_id="opp_001",
            source_id=SOURCE,
        )
        assert p1.pack_id == p2.pack_id
        assert p1.pack_id.startswith("proofpack_")

    def test_with_outcome_proof(self):
        proof = _make_proof()
        pack = build_proof_pack(
            tenant_id=TENANT,
            entity_type="opportunity",
            entity_id="opp_001",
            proofs=[proof],
            source_id=SOURCE,
        )
        assert pack.proof_count == 1
        assert pack.has_outcome_proof is True
        assert pack.completeness == ProofCompletionStatus.PARTIAL

    def test_with_payment_proof(self):
        proof = _make_proof(
            proof_type=ProofType.PAYMENT_EVIDENCE,
            source_event_type=ProofSourceEventType.PAYMENT_CONFIRMED,
            evidence_ref="payment_001",
        )
        pack = build_proof_pack(
            tenant_id=TENANT,
            entity_type="opportunity",
            entity_id="opp_001",
            proofs=[proof],
            source_id=SOURCE,
        )
        assert pack.has_payment_proof is True
        assert pack.revenue_state == EvidenceState.PAYMENT_EVIDENCED

    def test_with_delivery_proof(self):
        proof = _make_proof(
            proof_type=ProofType.DELIVERY_EVIDENCE,
            source_event_type=ProofSourceEventType.DELIVERY_TASK_COMPLETED,
            evidence_ref="delivery_001",
        )
        pack = build_proof_pack(
            tenant_id=TENANT,
            entity_type="opportunity",
            entity_id="opp_001",
            proofs=[proof],
            source_id=SOURCE,
        )
        assert pack.has_delivery_proof is True
        assert pack.delivery_state == EvidenceState.DELIVERY_EVIDENCED

    def test_complete_pack(self):
        outcome_proof = _make_proof(evidence_ref="ev_outcome")
        payment_proof = _make_proof(
            proof_type=ProofType.PAYMENT_EVIDENCE,
            source_event_type=ProofSourceEventType.PAYMENT_CONFIRMED,
            evidence_ref="ev_payment",
        )
        delivery_proof = _make_proof(
            proof_type=ProofType.DELIVERY_EVIDENCE,
            source_event_type=ProofSourceEventType.DELIVERY_TASK_COMPLETED,
            evidence_ref="ev_delivery",
        )
        pack = build_proof_pack(
            tenant_id=TENANT,
            entity_type="opportunity",
            entity_id="opp_001",
            proofs=[outcome_proof, payment_proof, delivery_proof],
            source_id=SOURCE,
        )
        assert pack.completeness == ProofCompletionStatus.COMPLETE
        assert pack.has_payment_proof is True
        assert pack.has_delivery_proof is True
        assert pack.has_outcome_proof is True

    def test_cross_tenant_filtered(self):
        other_proof = _make_proof(
            tenant_id="other_tenant",
            evidence_ref="other_ev",
        )
        pack = build_proof_pack(
            tenant_id=TENANT,
            entity_type="opportunity",
            entity_id="opp_001",
            proofs=[other_proof],
            source_id=SOURCE,
        )
        assert pack.proof_count == 0


# -----------------------------------------------------------------------
# Evidence assessment
# -----------------------------------------------------------------------


class TestEvidenceAssessment:
    def test_no_evidence_absent(self):
        assessment = assess_evidence_strength(
            tenant_id=TENANT,
            claim="strong product market fit",
            source_id=SOURCE,
        )
        assert isinstance(assessment, EvidenceAssessment)
        assert assessment.strength == EvidenceStrength.ABSENT

    def test_conclusive_evidence(self):
        assessment = assess_evidence_strength(
            tenant_id=TENANT,
            claim="customer satisfaction",
            evidence_refs=("ref_1", "ref_2", "ref_3"),
            confidence=0.9,
            source_id=SOURCE,
        )
        assert assessment.strength == EvidenceStrength.CONCLUSIVE

    def test_revenue_claim_needs_payment(self):
        assessment = assess_evidence_strength(
            tenant_id=TENANT,
            claim="revenue from client X",
            evidence_refs=("ref_1",),
            has_payment_proof=False,
            source_id=SOURCE,
        )
        assert any("payment evidence" in gap for gap in assessment.gaps)

    def test_delivery_claim_needs_proof(self):
        assessment = assess_evidence_strength(
            tenant_id=TENANT,
            claim="delivery completed for pilot",
            evidence_refs=("ref_1",),
            has_delivery_proof=False,
            source_id=SOURCE,
        )
        assert any("delivery evidence" in gap for gap in assessment.gaps)

    def test_deterministic_id(self):
        a1 = assess_evidence_strength(
            tenant_id=TENANT, claim="test", source_id=SOURCE,
        )
        a2 = assess_evidence_strength(
            tenant_id=TENANT, claim="test", source_id=SOURCE,
        )
        assert a1.assessment_id == a2.assessment_id
        assert a1.assessment_id.startswith("evassess_")


# -----------------------------------------------------------------------
# Proof completeness
# -----------------------------------------------------------------------


class TestProofCompleteness:
    def test_complete_when_all_present(self):
        proof = _make_proof()
        result = check_proof_completeness(
            tenant_id=TENANT,
            entity_type="opportunity",
            entity_id="opp_001",
            required_proof_types=["outcome_evidence"],
            proofs=[proof],
            source_id=SOURCE,
        )
        assert isinstance(result, ProofCompleteness)
        assert result.status == ProofCompletionStatus.COMPLETE
        assert result.completion_pct == 1.0

    def test_partial_when_some_missing(self):
        proof = _make_proof()
        result = check_proof_completeness(
            tenant_id=TENANT,
            entity_type="opportunity",
            entity_id="opp_001",
            required_proof_types=[
                "outcome_evidence", "payment_evidence",
            ],
            proofs=[proof],
            source_id=SOURCE,
        )
        assert result.status == ProofCompletionStatus.PARTIAL
        assert "payment_evidence" in result.missing_proof_types
        assert result.completion_pct == 0.5

    def test_missing_when_none_present(self):
        result = check_proof_completeness(
            tenant_id=TENANT,
            entity_type="opportunity",
            entity_id="opp_001",
            required_proof_types=["outcome_evidence"],
            proofs=[],
            source_id=SOURCE,
        )
        assert result.status == ProofCompletionStatus.MISSING
        assert result.completion_pct == 0.0

    def test_deterministic_id(self):
        c1 = check_proof_completeness(
            tenant_id=TENANT,
            entity_type="opportunity",
            entity_id="opp_001",
            source_id=SOURCE,
        )
        c2 = check_proof_completeness(
            tenant_id=TENANT,
            entity_type="opportunity",
            entity_id="opp_001",
            source_id=SOURCE,
        )
        assert c1.check_id == c2.check_id
        assert c1.check_id.startswith("proofcheck_")


# -----------------------------------------------------------------------
# Safety invariants
# -----------------------------------------------------------------------


class TestProofEngineSafety:
    def test_pack_payment_consistency(self):
        """Cannot claim PAYMENT_EVIDENCED without payment proof."""
        with pytest.raises(ValueError, match="cannot claim PAYMENT_EVIDENCED"):
            ProofPack(
                tenant_id=TENANT,
                pack_id="proofpack_fake",
                entity_type="opportunity",
                entity_id="opp_001",
                has_payment_proof=False,
                revenue_state=EvidenceState.PAYMENT_EVIDENCED,
                source_id=SOURCE,
            )

    def test_pack_delivery_consistency(self):
        """Cannot claim DELIVERY_EVIDENCED without delivery proof."""
        with pytest.raises(ValueError, match="cannot claim DELIVERY_EVIDENCED"):
            ProofPack(
                tenant_id=TENANT,
                pack_id="proofpack_fake",
                entity_type="opportunity",
                entity_id="opp_001",
                has_delivery_proof=False,
                delivery_state=EvidenceState.DELIVERY_EVIDENCED,
                source_id=SOURCE,
            )

    def test_pack_publication_requires_proofs(self):
        """Cannot be publication-ready with no proofs."""
        with pytest.raises(ValueError, match="publication-ready with no proofs"):
            ProofPack(
                tenant_id=TENANT,
                pack_id="proofpack_fake",
                entity_type="opportunity",
                entity_id="opp_001",
                proof_count=0,
                publication_ready=True,
                source_id=SOURCE,
            )

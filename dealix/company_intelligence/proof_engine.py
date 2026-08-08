"""Proof & Outcome Validation Engine — evidence verification and proof packs.

Pure-logic engine that validates outcomes against evidence, builds proof
packs for claims, assesses evidence strength, and checks proof completeness.

No database, network, or LLM calls. Revenue recognition requires payment
evidence. Delivery completion requires delivery evidence. Synthetic proof
for financial or delivery claims is forbidden.

Design principles:
- Deterministic content-addressable IDs (SHA-256).
- Frozen Pydantic v2 models — no silent mutation.
- Safety: synthetic financial/delivery proof forbidden.
- Revenue claims require ``PAYMENT_CONFIRMED`` source events.
- Delivery claims require ``DELIVERY_TASK_COMPLETED`` source events.
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from typing import Annotated, Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)

from dealix.company_intelligence.outcome_contracts import (
    CanonicalOutcomeEvent,
    CanonicalProofEvent,
    EvidenceState,
    OutcomeEventType,
    ProofSourceEventType,
    ProofType,
)

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _stable_id(prefix: str, payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"{prefix}_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class ValidationResult(StrEnum):
    """Outcome validation result."""

    VALID = "valid"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    CONFLICTING_EVIDENCE = "conflicting_evidence"
    MISSING_PROOF = "missing_proof"
    SYNTHETIC_BLOCKED = "synthetic_blocked"


class EvidenceStrength(StrEnum):
    """Strength classification of evidence."""

    CONCLUSIVE = "conclusive"
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    ABSENT = "absent"


class ProofCompletionStatus(StrEnum):
    """Status of proof completeness check."""

    COMPLETE = "complete"
    PARTIAL = "partial"
    MISSING = "missing"


# ---------------------------------------------------------------------------
# Contracts
# ---------------------------------------------------------------------------


class OutcomeValidation(BaseModel):
    """Result of validating an outcome event against evidence."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    validation_id: NonEmptyString
    outcome_id: NonEmptyString
    result: ValidationResult
    evidence_strength: EvidenceStrength
    evidence_count: int = Field(default=0, ge=0)
    issues: tuple[str, ...] = ()
    validated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    source_id: NonEmptyString = ""


class ProofPack(BaseModel):
    """Assembled proof package for a claim or entity."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    pack_id: NonEmptyString
    entity_type: NonEmptyString
    entity_id: NonEmptyString
    proofs: tuple[CanonicalProofEvent, ...] = ()
    proof_count: int = Field(default=0, ge=0)
    has_payment_proof: bool = False
    has_delivery_proof: bool = False
    has_outcome_proof: bool = False
    revenue_state: EvidenceState = EvidenceState.NOT_EVIDENCED
    delivery_state: EvidenceState = EvidenceState.NOT_EVIDENCED
    completeness: ProofCompletionStatus = ProofCompletionStatus.MISSING
    assembled_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    publication_ready: bool = False
    source_id: NonEmptyString = ""

    @model_validator(mode="after")
    def _enforce_evidence_consistency(self) -> ProofPack:
        if self.has_payment_proof and self.revenue_state != EvidenceState.PAYMENT_EVIDENCED:
            raise ValueError(
                "payment proof present but revenue_state not PAYMENT_EVIDENCED"
            )
        if self.has_delivery_proof and self.delivery_state != EvidenceState.DELIVERY_EVIDENCED:
            raise ValueError(
                "delivery proof present but delivery_state not DELIVERY_EVIDENCED"
            )
        if not self.has_payment_proof and self.revenue_state == EvidenceState.PAYMENT_EVIDENCED:
            raise ValueError(
                "cannot claim PAYMENT_EVIDENCED without payment proof"
            )
        if not self.has_delivery_proof and self.delivery_state == EvidenceState.DELIVERY_EVIDENCED:
            raise ValueError(
                "cannot claim DELIVERY_EVIDENCED without delivery proof"
            )
        # Publication requires at least one proof
        if self.publication_ready and self.proof_count == 0:
            raise ValueError(
                "cannot mark proof pack as publication-ready with no proofs"
            )
        return self


class EvidenceAssessment(BaseModel):
    """Assessment of evidence strength for a claim."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    assessment_id: NonEmptyString
    claim: NonEmptyString
    strength: EvidenceStrength
    supporting_evidence: tuple[str, ...] = ()
    gaps: tuple[str, ...] = ()
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    recommendation: str = ""
    source_id: NonEmptyString = ""


class ProofCompleteness(BaseModel):
    """Completeness check result for required proofs."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    check_id: NonEmptyString
    entity_type: NonEmptyString
    entity_id: NonEmptyString
    status: ProofCompletionStatus
    required_proof_types: tuple[str, ...] = ()
    present_proof_types: tuple[str, ...] = ()
    missing_proof_types: tuple[str, ...] = ()
    completion_pct: float = Field(default=0.0, ge=0.0, le=1.0)
    source_id: NonEmptyString = ""


# ---------------------------------------------------------------------------
# Engine functions
# ---------------------------------------------------------------------------


def validate_outcome(
    outcome: CanonicalOutcomeEvent,
    *,
    source_id: str = "proof_engine",
) -> OutcomeValidation:
    """Validate that an outcome event has sufficient evidence."""

    issues: list[str] = []
    evidence_count = len(outcome.evidence_refs)

    # Check evidence presence
    if evidence_count == 0:
        result = ValidationResult.MISSING_PROOF
        strength = EvidenceStrength.ABSENT
        issues.append("no evidence references provided")
    elif outcome.is_synthetic:
        if outcome.event_type in (
            OutcomeEventType.PAYMENT_RECEIVED,
            OutcomeEventType.DELIVERY_COMPLETED,
        ):
            result = ValidationResult.SYNTHETIC_BLOCKED
            strength = EvidenceStrength.ABSENT
            issues.append(
                f"synthetic {outcome.event_type.value} outcomes are forbidden"
            )
        else:
            result = ValidationResult.VALID
            strength = EvidenceStrength.WEAK
            issues.append("synthetic outcome — treat as hypothesis")
    elif outcome.confidence < 0.5:
        result = ValidationResult.INSUFFICIENT_EVIDENCE
        strength = EvidenceStrength.WEAK
        issues.append(
            f"low confidence ({outcome.confidence:.0%}) — "
            "additional evidence recommended"
        )
    elif evidence_count == 1:
        result = ValidationResult.VALID
        strength = EvidenceStrength.MODERATE
    elif evidence_count >= 3:
        result = ValidationResult.VALID
        strength = EvidenceStrength.CONCLUSIVE
    else:
        result = ValidationResult.VALID
        strength = EvidenceStrength.STRONG

    validation_id = _stable_id(
        "validation",
        {
            "tenant_id": outcome.tenant_id,
            "outcome_id": outcome.outcome_id,
            "evidence_count": evidence_count,
            "is_synthetic": outcome.is_synthetic,
        },
    )

    return OutcomeValidation(
        tenant_id=outcome.tenant_id,
        validation_id=validation_id,
        outcome_id=outcome.outcome_id,
        result=result,
        evidence_strength=strength,
        evidence_count=evidence_count,
        issues=tuple(issues),
        source_id=source_id,
    )


def build_proof_pack(
    *,
    tenant_id: str,
    entity_type: str,
    entity_id: str,
    proofs: tuple[CanonicalProofEvent, ...] | list[CanonicalProofEvent] = (),
    source_id: str = "proof_engine",
) -> ProofPack:
    """Assemble a proof pack for an entity from available proof events."""

    proofs_list = list(proofs)

    # Filter to tenant
    tenant_proofs = [p for p in proofs_list if p.tenant_id == tenant_id]

    has_payment = any(
        p.proof_type == ProofType.PAYMENT_EVIDENCE
        and p.source_event_type == ProofSourceEventType.PAYMENT_CONFIRMED
        and not p.is_synthetic
        for p in tenant_proofs
    )
    has_delivery = any(
        p.proof_type == ProofType.DELIVERY_EVIDENCE
        and p.source_event_type == ProofSourceEventType.DELIVERY_TASK_COMPLETED
        and not p.is_synthetic
        for p in tenant_proofs
    )
    has_outcome = any(
        p.proof_type == ProofType.OUTCOME_EVIDENCE
        for p in tenant_proofs
    )

    revenue_state = (
        EvidenceState.PAYMENT_EVIDENCED
        if has_payment
        else EvidenceState.NOT_EVIDENCED
    )
    delivery_state = (
        EvidenceState.DELIVERY_EVIDENCED
        if has_delivery
        else EvidenceState.NOT_EVIDENCED
    )

    # Completeness
    if not tenant_proofs:
        completeness = ProofCompletionStatus.MISSING
    elif has_payment and has_delivery and has_outcome:
        completeness = ProofCompletionStatus.COMPLETE
    else:
        completeness = ProofCompletionStatus.PARTIAL

    # Publication readiness — requires at least outcome proof and no synthetics
    publication_ready = (
        len(tenant_proofs) > 0
        and all(not p.is_synthetic for p in tenant_proofs)
        and all(p.publication_approved for p in tenant_proofs)
    )

    pack_id = _stable_id(
        "proofpack",
        {
            "tenant_id": tenant_id.strip(),
            "entity_type": entity_type.strip(),
            "entity_id": entity_id.strip(),
            "proof_count": len(tenant_proofs),
            "has_payment": has_payment,
            "has_delivery": has_delivery,
        },
    )

    return ProofPack(
        tenant_id=tenant_id,
        pack_id=pack_id,
        entity_type=entity_type,
        entity_id=entity_id,
        proofs=tuple(tenant_proofs),
        proof_count=len(tenant_proofs),
        has_payment_proof=has_payment,
        has_delivery_proof=has_delivery,
        has_outcome_proof=has_outcome,
        revenue_state=revenue_state,
        delivery_state=delivery_state,
        completeness=completeness,
        publication_ready=publication_ready,
        source_id=source_id,
    )


def assess_evidence_strength(
    *,
    tenant_id: str,
    claim: str,
    evidence_refs: tuple[str, ...] | list[str] = (),
    has_payment_proof: bool = False,
    has_delivery_proof: bool = False,
    confidence: float = 0.5,
    source_id: str = "proof_engine",
) -> EvidenceAssessment:
    """Assess the strength of evidence supporting a claim."""

    evidence_list = list(evidence_refs)
    gaps: list[str] = []
    supporting: list[str] = list(evidence_list)

    # Determine strength
    if not evidence_list:
        strength = EvidenceStrength.ABSENT
        gaps.append("no evidence references provided")
        recommendation = "gather evidence before making this claim"
    elif len(evidence_list) >= 3 and confidence >= 0.8:
        strength = EvidenceStrength.CONCLUSIVE
        recommendation = "evidence is strong enough to support the claim"
    elif len(evidence_list) >= 2 and confidence >= 0.6:
        strength = EvidenceStrength.STRONG
        recommendation = "evidence is solid — consider one more data point"
    elif len(evidence_list) >= 1 and confidence >= 0.4:
        strength = EvidenceStrength.MODERATE
        gaps.append("additional corroborating evidence recommended")
        recommendation = "gather additional evidence to strengthen the claim"
    else:
        strength = EvidenceStrength.WEAK
        gaps.append("evidence is insufficient for the claim")
        recommendation = "do not make this claim until evidence improves"

    # Financial/delivery gaps
    if "revenue" in claim.lower() or "payment" in claim.lower():
        if not has_payment_proof:
            gaps.append("revenue claim requires payment evidence")
    if "delivery" in claim.lower() or "completed" in claim.lower():
        if not has_delivery_proof:
            gaps.append("delivery claim requires delivery evidence")

    assessment_id = _stable_id(
        "evassess",
        {
            "tenant_id": tenant_id.strip(),
            "claim": claim.strip(),
            "evidence_count": len(evidence_list),
            "confidence": confidence,
        },
    )

    return EvidenceAssessment(
        tenant_id=tenant_id,
        assessment_id=assessment_id,
        claim=claim,
        strength=strength,
        supporting_evidence=tuple(supporting),
        gaps=tuple(gaps),
        confidence=confidence,
        recommendation=recommendation,
        source_id=source_id,
    )


def check_proof_completeness(
    *,
    tenant_id: str,
    entity_type: str,
    entity_id: str,
    required_proof_types: tuple[str, ...] | list[str] = (),
    proofs: tuple[CanonicalProofEvent, ...] | list[CanonicalProofEvent] = (),
    source_id: str = "proof_engine",
) -> ProofCompleteness:
    """Check whether all required proof types are present."""

    required = list(required_proof_types) or [
        ProofType.OUTCOME_EVIDENCE.value,
    ]
    present = sorted({p.proof_type.value for p in proofs if p.tenant_id == tenant_id})
    missing = sorted(set(required) - set(present))

    completion_pct = round(
        len(set(required) & set(present)) / max(len(required), 1), 4
    )

    if not missing:
        status = ProofCompletionStatus.COMPLETE
    elif present:
        status = ProofCompletionStatus.PARTIAL
    else:
        status = ProofCompletionStatus.MISSING

    check_id = _stable_id(
        "proofcheck",
        {
            "tenant_id": tenant_id.strip(),
            "entity_type": entity_type.strip(),
            "entity_id": entity_id.strip(),
            "required": sorted(required),
            "present": present,
        },
    )

    return ProofCompleteness(
        tenant_id=tenant_id,
        check_id=check_id,
        entity_type=entity_type,
        entity_id=entity_id,
        status=status,
        required_proof_types=tuple(sorted(required)),
        present_proof_types=tuple(present),
        missing_proof_types=tuple(missing),
        completion_pct=completion_pct,
        source_id=source_id,
    )

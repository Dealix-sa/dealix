"""Canonical outcome, proof, learning, and executive-command contracts.

The models are persistence-neutral and contain no transport, storage, or
external-execution capability. Financial and delivery state is derived only
from fully revalidated, non-synthetic proof events.
"""
from __future__ import annotations

import json
from datetime import UTC, date, datetime
from enum import StrEnum
from hashlib import sha256
from typing import Annotated, Any, Iterable

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class OutcomeEventType(StrEnum):
    PROSPECT_REPLIED = "prospect_replied"
    NO_REPLY = "no_reply"
    OBJECTION_RECORDED = "objection_recorded"
    MEETING_BOOKED = "meeting_booked"
    PROPOSAL_REVIEWED = "proposal_reviewed"
    PAYMENT_RECEIVED = "payment_received"
    DELIVERY_COMPLETED = "delivery_completed"
    TECHNICAL_FAILURE = "technical_failure"
    TECHNICAL_FIX_VERIFIED = "technical_fix_verified"


class ProofType(StrEnum):
    OUTCOME_EVIDENCE = "outcome_evidence"
    PAYMENT_EVIDENCE = "payment_evidence"
    DELIVERY_EVIDENCE = "delivery_evidence"
    TECHNICAL_VERIFICATION = "technical_verification"


class ProofSourceEventType(StrEnum):
    """Ledger events allowed to establish financial or delivery truth."""

    PAYMENT_CONFIRMED = "payment_confirmed"
    DELIVERY_TASK_COMPLETED = "delivery_task_completed"


class LearningEventType(StrEnum):
    TARGETING = "targeting"
    MESSAGE = "message"
    NEGOTIATION = "negotiation"
    OFFER = "offer"
    DELIVERY = "delivery"
    TECHNICAL = "technical"
    DATA_QUALITY = "data_quality"


class EvidenceState(StrEnum):
    NOT_EVIDENCED = "not_evidenced"
    PAYMENT_EVIDENCED = "payment_evidenced"
    DELIVERY_EVIDENCED = "delivery_evidenced"


def _normalized_refs(refs: Iterable[str]) -> list[str]:
    normalized = sorted({item.strip() for item in refs if item.strip()})
    if not normalized:
        raise ValueError("at least one non-empty evidence reference is required")
    return normalized


def _sorted_unique(values: Iterable[str]) -> list[str]:
    return sorted({item.strip() for item in values if item.strip()})


def _stable_id(prefix: str, payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"{prefix}_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


class CanonicalOutcomeEvent(BaseModel):
    """A real or explicitly synthetic result linked to one internal action."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    outcome_id: NonEmptyString
    action_id: NonEmptyString
    event_type: OutcomeEventType
    occurred_at: datetime
    evidence_refs: list[NonEmptyString] = Field(..., min_length=1)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    is_synthetic: bool = False
    notes: str = ""

    @model_validator(mode="after")
    def enforce_integrity(self) -> CanonicalOutcomeEvent:
        normalized = _normalized_refs(self.evidence_refs)
        if self.evidence_refs != normalized:
            raise ValueError("evidence_refs must be sorted and unique")
        if self.is_synthetic and self.event_type in {
            OutcomeEventType.PAYMENT_RECEIVED,
            OutcomeEventType.DELIVERY_COMPLETED,
        }:
            raise ValueError("synthetic financial or delivery outcomes are forbidden")
        expected_id = _stable_id(
            "outcome",
            {
                "action_id": self.action_id,
                "event_type": self.event_type.value,
                "evidence_refs": self.evidence_refs,
                "is_synthetic": self.is_synthetic,
                "occurred_at": self.occurred_at.isoformat(),
                "tenant_id": self.tenant_id,
            },
        )
        if self.outcome_id != expected_id:
            raise ValueError("outcome_id does not match the canonical payload")
        return self


class CanonicalProofEvent(BaseModel):
    """Verified evidence used for value, payment, delivery, or technical truth."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    proof_id: NonEmptyString
    entity_type: NonEmptyString
    entity_id: NonEmptyString
    proof_type: ProofType
    evidence_ref: NonEmptyString
    source_event_type: ProofSourceEventType | None = None
    verified_at: datetime
    source_outcome_id: str | None = None
    verifier: NonEmptyString
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    is_synthetic: bool = False
    publication_approved: bool = False

    @model_validator(mode="after")
    def enforce_integrity(self) -> CanonicalProofEvent:
        required_source = {
            ProofType.PAYMENT_EVIDENCE: ProofSourceEventType.PAYMENT_CONFIRMED,
            ProofType.DELIVERY_EVIDENCE: ProofSourceEventType.DELIVERY_TASK_COMPLETED,
        }.get(self.proof_type)
        if required_source is not None and self.source_event_type != required_source:
            raise ValueError(
                f"{self.proof_type.value} requires source event {required_source.value}"
            )
        if self.is_synthetic and self.proof_type in {
            ProofType.PAYMENT_EVIDENCE,
            ProofType.DELIVERY_EVIDENCE,
        }:
            raise ValueError("synthetic payment or delivery proof is forbidden")
        expected_id = _stable_id(
            "proof",
            {
                "entity_id": self.entity_id,
                "entity_type": self.entity_type,
                "evidence_ref": self.evidence_ref,
                "proof_type": self.proof_type.value,
                "source_event_type": (
                    self.source_event_type.value
                    if self.source_event_type is not None
                    else None
                ),
                "source_outcome_id": self.source_outcome_id,
                "tenant_id": self.tenant_id,
                "verified_at": self.verified_at.isoformat(),
                "verifier": self.verifier,
            },
        )
        if self.proof_id != expected_id:
            raise ValueError("proof_id does not match the canonical payload")
        return self


class CanonicalLearningEvent(BaseModel):
    """Evidence-bounded improvement proposal that cannot mutate policy itself."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    learning_id: NonEmptyString
    event_type: LearningEventType
    evidence_refs: list[NonEmptyString] = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)
    recommended_change: NonEmptyString
    hypothesis_only: bool = True
    approval_required: bool = True
    applied: bool = False
    official_policy_change_allowed: bool = False
    created_at: datetime

    @model_validator(mode="after")
    def enforce_governance(self) -> CanonicalLearningEvent:
        normalized = _normalized_refs(self.evidence_refs)
        if self.evidence_refs != normalized:
            raise ValueError("evidence_refs must be sorted and unique")
        if not self.approval_required:
            raise ValueError("learning recommendations require approval")
        if self.applied:
            raise ValueError("canonical learning events are proposals, not mutations")
        if self.official_policy_change_allowed:
            raise ValueError("learning cannot grant official policy authority")
        expected_id = _stable_id(
            "learning",
            {
                "created_at": self.created_at.isoformat(),
                "event_type": self.event_type.value,
                "evidence_refs": self.evidence_refs,
                "recommended_change": self.recommended_change,
                "tenant_id": self.tenant_id,
            },
        )
        if self.learning_id != expected_id:
            raise ValueError("learning_id does not match the canonical payload")
        return self


def _revalidate_proof(proof: CanonicalProofEvent) -> CanonicalProofEvent:
    """Re-run every proof invariant from raw values at a recognition boundary."""

    return CanonicalProofEvent.model_validate(proof.model_dump(mode="python"))


class CanonicalDailyCommand(BaseModel):
    """One deterministic executive readout for a tenant and calendar date."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    command_id: NonEmptyString
    command_date: date
    priorities: list[NonEmptyString] = Field(default_factory=list)
    approval_items: list[NonEmptyString] = Field(default_factory=list)
    proofs: list[CanonicalProofEvent] = Field(default_factory=list)
    proof_ids: list[NonEmptyString] = Field(default_factory=list)
    payment_proof_ids: list[NonEmptyString] = Field(default_factory=list)
    delivery_proof_ids: list[NonEmptyString] = Field(default_factory=list)
    learning_ids: list[NonEmptyString] = Field(default_factory=list)
    revenue_state: EvidenceState = EvidenceState.NOT_EVIDENCED
    delivery_state: EvidenceState = EvidenceState.NOT_EVIDENCED
    recognized_revenue: bool = False
    delivery_completed: bool = False
    generated_at: datetime

    @model_validator(mode="after")
    def enforce_evidence_states(self) -> CanonicalDailyCommand:
        for name, values in (
            ("priorities", self.priorities),
            ("approval_items", self.approval_items),
            ("proof_ids", self.proof_ids),
            ("payment_proof_ids", self.payment_proof_ids),
            ("delivery_proof_ids", self.delivery_proof_ids),
            ("learning_ids", self.learning_ids),
        ):
            if values != _sorted_unique(values):
                raise ValueError(f"{name} must be sorted and unique")

        proof_ids = set(self.proof_ids)
        if not set(self.payment_proof_ids).issubset(proof_ids):
            raise ValueError("payment_proof_ids must be included in proof_ids")
        if not set(self.delivery_proof_ids).issubset(proof_ids):
            raise ValueError("delivery_proof_ids must be included in proof_ids")

        validated_proofs = [_revalidate_proof(proof) for proof in self.proofs]
        if validated_proofs and any(
            proof.tenant_id != self.tenant_id for proof in validated_proofs
        ):
            raise ValueError("cross-tenant proof is forbidden")

        typed_proof_ids = sorted({proof.proof_id for proof in validated_proofs})
        typed_payment_ids = sorted(
            {
                proof.proof_id
                for proof in validated_proofs
                if proof.proof_type == ProofType.PAYMENT_EVIDENCE
                and proof.source_event_type == ProofSourceEventType.PAYMENT_CONFIRMED
                and not proof.is_synthetic
            }
        )
        typed_delivery_ids = sorted(
            {
                proof.proof_id
                for proof in validated_proofs
                if proof.proof_type == ProofType.DELIVERY_EVIDENCE
                and proof.source_event_type
                == ProofSourceEventType.DELIVERY_TASK_COMPLETED
                and not proof.is_synthetic
            }
        )
        if self.proof_ids != typed_proof_ids:
            raise ValueError("proof_ids must match typed proof objects")
        if self.payment_proof_ids != typed_payment_ids:
            raise ValueError("payment_proof_ids must reference typed payment proofs")
        if self.delivery_proof_ids != typed_delivery_ids:
            raise ValueError("delivery_proof_ids must reference typed delivery proofs")

        has_payment = bool(typed_payment_ids)
        has_delivery = bool(typed_delivery_ids)
        expected_revenue_state = (
            EvidenceState.PAYMENT_EVIDENCED
            if has_payment
            else EvidenceState.NOT_EVIDENCED
        )
        expected_delivery_state = (
            EvidenceState.DELIVERY_EVIDENCED
            if has_delivery
            else EvidenceState.NOT_EVIDENCED
        )
        if self.revenue_state != expected_revenue_state or (
            self.recognized_revenue != has_payment
        ):
            raise ValueError("recognized revenue requires referenced payment proof")
        if self.delivery_state != expected_delivery_state or (
            self.delivery_completed != has_delivery
        ):
            raise ValueError("completed delivery requires referenced delivery proof")

        expected_id = _stable_id(
            "command",
            {
                "approval_items": self.approval_items,
                "command_date": self.command_date.isoformat(),
                "delivery_proof_ids": self.delivery_proof_ids,
                "delivery_state": self.delivery_state.value,
                "learning_ids": self.learning_ids,
                "payment_proof_ids": self.payment_proof_ids,
                "priorities": self.priorities,
                "proof_ids": self.proof_ids,
                "revenue_state": self.revenue_state.value,
                "tenant_id": self.tenant_id,
            },
        )
        if self.command_id != expected_id:
            raise ValueError("command_id does not match the canonical payload")
        return self


def build_outcome_event(
    *,
    tenant_id: str,
    action_id: str,
    event_type: OutcomeEventType,
    occurred_at: datetime,
    evidence_refs: list[str],
    confidence: float = 1.0,
    is_synthetic: bool = False,
    notes: str = "",
) -> CanonicalOutcomeEvent:
    normalized = _normalized_refs(evidence_refs)
    outcome_id = _stable_id(
        "outcome",
        {
            "action_id": action_id.strip(),
            "event_type": event_type.value,
            "evidence_refs": normalized,
            "is_synthetic": is_synthetic,
            "occurred_at": occurred_at.isoformat(),
            "tenant_id": tenant_id.strip(),
        },
    )
    return CanonicalOutcomeEvent(
        tenant_id=tenant_id,
        outcome_id=outcome_id,
        action_id=action_id,
        event_type=event_type,
        occurred_at=occurred_at,
        evidence_refs=normalized,
        confidence=confidence,
        is_synthetic=is_synthetic,
        notes=notes,
    )


def build_proof_event(
    *,
    tenant_id: str,
    entity_type: str,
    entity_id: str,
    proof_type: ProofType,
    evidence_ref: str,
    verified_at: datetime,
    verifier: str,
    source_event_type: ProofSourceEventType | None = None,
    source_outcome_id: str | None = None,
    confidence: float = 1.0,
    is_synthetic: bool = False,
    publication_approved: bool = False,
) -> CanonicalProofEvent:
    proof_id = _stable_id(
        "proof",
        {
            "entity_id": entity_id.strip(),
            "entity_type": entity_type.strip(),
            "evidence_ref": evidence_ref.strip(),
            "proof_type": proof_type.value,
            "source_event_type": (
                source_event_type.value if source_event_type is not None else None
            ),
            "source_outcome_id": source_outcome_id,
            "tenant_id": tenant_id.strip(),
            "verified_at": verified_at.isoformat(),
            "verifier": verifier.strip(),
        },
    )
    return CanonicalProofEvent(
        tenant_id=tenant_id,
        proof_id=proof_id,
        entity_type=entity_type,
        entity_id=entity_id,
        proof_type=proof_type,
        evidence_ref=evidence_ref,
        source_event_type=source_event_type,
        verified_at=verified_at,
        verifier=verifier,
        source_outcome_id=source_outcome_id,
        confidence=confidence,
        is_synthetic=is_synthetic,
        publication_approved=publication_approved,
    )


def build_learning_event(
    *,
    tenant_id: str,
    event_type: LearningEventType,
    evidence_refs: list[str],
    confidence: float,
    recommended_change: str,
    created_at: datetime,
    hypothesis_only: bool = True,
) -> CanonicalLearningEvent:
    normalized = _normalized_refs(evidence_refs)
    learning_id = _stable_id(
        "learning",
        {
            "created_at": created_at.isoformat(),
            "event_type": event_type.value,
            "evidence_refs": normalized,
            "recommended_change": recommended_change.strip(),
            "tenant_id": tenant_id.strip(),
        },
    )
    return CanonicalLearningEvent(
        tenant_id=tenant_id,
        learning_id=learning_id,
        event_type=event_type,
        evidence_refs=normalized,
        confidence=confidence,
        recommended_change=recommended_change,
        hypothesis_only=hypothesis_only,
        approval_required=True,
        applied=False,
        official_policy_change_allowed=False,
        created_at=created_at,
    )


def build_daily_command(
    *,
    tenant_id: str,
    command_date: date,
    priorities: list[str],
    approval_items: list[str],
    proofs: list[CanonicalProofEvent],
    learning_events: list[CanonicalLearningEvent],
    generated_at: datetime | None = None,
) -> CanonicalDailyCommand:
    """Build a deterministic command after revalidating all supplied proof truth."""

    validated_proofs = [_revalidate_proof(proof) for proof in proofs]
    if any(proof.tenant_id != tenant_id for proof in validated_proofs):
        raise ValueError("cross-tenant proof is forbidden")
    if any(event.tenant_id != tenant_id for event in learning_events):
        raise ValueError("cross-tenant learning is forbidden")

    normalized_priorities = _sorted_unique(priorities)
    normalized_approvals = _sorted_unique(approval_items)
    proof_ids = sorted({proof.proof_id for proof in validated_proofs})
    payment_proof_ids = sorted(
        {
            proof.proof_id
            for proof in validated_proofs
            if proof.proof_type == ProofType.PAYMENT_EVIDENCE
            and proof.source_event_type == ProofSourceEventType.PAYMENT_CONFIRMED
            and not proof.is_synthetic
        }
    )
    delivery_proof_ids = sorted(
        {
            proof.proof_id
            for proof in validated_proofs
            if proof.proof_type == ProofType.DELIVERY_EVIDENCE
            and proof.source_event_type
            == ProofSourceEventType.DELIVERY_TASK_COMPLETED
            and not proof.is_synthetic
        }
    )
    learning_ids = sorted({event.learning_id for event in learning_events})

    has_payment = bool(payment_proof_ids)
    has_delivery = bool(delivery_proof_ids)
    revenue_state = (
        EvidenceState.PAYMENT_EVIDENCED if has_payment else EvidenceState.NOT_EVIDENCED
    )
    delivery_state = (
        EvidenceState.DELIVERY_EVIDENCED if has_delivery else EvidenceState.NOT_EVIDENCED
    )
    command_id = _stable_id(
        "command",
        {
            "approval_items": normalized_approvals,
            "command_date": command_date.isoformat(),
            "delivery_proof_ids": delivery_proof_ids,
            "delivery_state": delivery_state.value,
            "learning_ids": learning_ids,
            "payment_proof_ids": payment_proof_ids,
            "priorities": normalized_priorities,
            "proof_ids": proof_ids,
            "revenue_state": revenue_state.value,
            "tenant_id": tenant_id.strip(),
        },
    )
    return CanonicalDailyCommand(
        tenant_id=tenant_id,
        command_id=command_id,
        command_date=command_date,
        priorities=normalized_priorities,
        approval_items=normalized_approvals,
        proofs=validated_proofs,
        proof_ids=proof_ids,
        payment_proof_ids=payment_proof_ids,
        delivery_proof_ids=delivery_proof_ids,
        learning_ids=learning_ids,
        revenue_state=revenue_state,
        delivery_state=delivery_state,
        recognized_revenue=has_payment,
        delivery_completed=has_delivery,
        generated_at=generated_at or datetime.now(UTC),
    )

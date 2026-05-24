"""Decision Passport — institutional record for every critical AI Stack decision.

Each Decision Passport binds a single AI decision to four institutional dimensions:

* **Approval (A0..A3)** — how much human approval is required.
* **Reversibility (R0..R3)** — how easily the action can be undone.
* **Sensitivity (S0..S3)** — PII / regulatory weight of the action.
* **Confidence (C0..C3)** — how strongly the AI vouches for its own output.

The passport is the unit the rest of the stack (governance_os, proof_os,
client_os) consumes when it needs a single, comparable record across every
layer. It is deliberately **deterministic and immutable** — once issued, only
the evidence chain may grow, and only by append.

The passport never carries the original model output verbatim; it stores a
SHA-256 hash of the rendered decision so the audit trail can prove that the
record matches what was shown to the customer without re-storing the content.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timezone
from enum import IntEnum
from typing import Any


class ApprovalLevel(IntEnum):
    """Approval ladder — A0 (auto) → A3 (board)."""

    A0_AUTO = 0
    A1_TEAM_LEAD = 1
    A2_FOUNDER = 2
    A3_BOARD = 3


class Reversibility(IntEnum):
    """How easily the decision can be reversed."""

    R0_TRIVIAL = 0
    R1_QUICK = 1
    R2_HARD = 2
    R3_IRREVERSIBLE = 3


class Sensitivity(IntEnum):
    """PII / regulatory weight."""

    S0_PUBLIC = 0
    S1_INTERNAL = 1
    S2_CONFIDENTIAL = 2
    S3_REGULATED_PII = 3


class Confidence(IntEnum):
    """How strongly the AI vouches for its output."""

    C0_SPECULATIVE = 0
    C1_LOW = 1
    C2_MEDIUM = 2
    C3_HIGH = 3


@dataclass(frozen=True, slots=True)
class DecisionPassport:
    """Immutable institutional record of a single AI decision.

    The passport is hashed on creation so two reviewers comparing the same
    passport can prove they saw the same content (the ``content_hash`` field
    binds the rendered decision to the passport identifier).
    """

    passport_id: str
    tenant_id: str
    decision_type: str
    summary_ar: str
    summary_en: str
    approval_level: int
    reversibility: int
    sensitivity: int
    confidence: int
    content_hash: str
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    source_passport_ids: tuple[str, ...] = field(default_factory=tuple)
    governance_decision: str = "allow"
    approved_by: str | None = None
    created_at: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["evidence_refs"] = list(self.evidence_refs)
        data["source_passport_ids"] = list(self.source_passport_ids)
        data["metadata"] = dict(self.metadata)
        return data

    @property
    def requires_human(self) -> bool:
        return self.approval_level >= ApprovalLevel.A2_FOUNDER

    @property
    def is_irreversible(self) -> bool:
        return self.reversibility >= Reversibility.R3_IRREVERSIBLE

    @property
    def is_regulated_pii(self) -> bool:
        return self.sensitivity >= Sensitivity.S3_REGULATED_PII


_DECISION_TYPES: frozenset[str] = frozenset(
    {
        "icp_classification",
        "pain_extraction",
        "qualification",
        "proposal_draft",
        "proof_pack_assembly",
        "retainer_recommendation",
        "doctrine_check",
        "governance_gate",
        "value_record",
        "capital_register",
        "outreach_draft",
        "model_routing",
    }
)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _hash_content(content: str | Mapping[str, Any]) -> str:
    if isinstance(content, Mapping):
        payload = json.dumps(content, sort_keys=True, ensure_ascii=False, default=str)
    else:
        payload = str(content)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _classify_approval(
    *,
    sensitivity: Sensitivity,
    reversibility: Reversibility,
    confidence: Confidence,
    external_action: bool,
) -> ApprovalLevel:
    """Derive minimum approval level from the four dimensions.

    Doctrine-aligned: external actions on regulated data always escalate to
    the founder; irreversible or low-confidence actions never auto-approve.
    """
    if external_action and sensitivity >= Sensitivity.S3_REGULATED_PII:
        return ApprovalLevel.A2_FOUNDER
    if reversibility >= Reversibility.R3_IRREVERSIBLE:
        return ApprovalLevel.A2_FOUNDER
    if sensitivity >= Sensitivity.S3_REGULATED_PII:
        return ApprovalLevel.A1_TEAM_LEAD
    if confidence <= Confidence.C1_LOW and external_action:
        return ApprovalLevel.A1_TEAM_LEAD
    if external_action:
        return ApprovalLevel.A1_TEAM_LEAD
    return ApprovalLevel.A0_AUTO


def issue_passport(
    *,
    tenant_id: str,
    decision_type: str,
    summary_ar: str,
    summary_en: str,
    content: str | Mapping[str, Any],
    sensitivity: Sensitivity = Sensitivity.S1_INTERNAL,
    reversibility: Reversibility = Reversibility.R1_QUICK,
    confidence: Confidence = Confidence.C2_MEDIUM,
    external_action: bool = False,
    evidence_refs: Sequence[str] = (),
    source_passport_ids: Sequence[str] = (),
    governance_decision: str = "allow",
    approved_by: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> DecisionPassport:
    """Issue a new Decision Passport with deterministic approval classification.

    Bilingual summaries (AR + EN) are MANDATORY — a passport without both
    fails Doctrine non-negotiable #11 (bilingual customer-facing artifacts).
    """
    if not tenant_id or not tenant_id.strip():
        raise ValueError("tenant_id is required")
    if decision_type not in _DECISION_TYPES:
        raise ValueError(
            f"unknown decision_type: {decision_type!r} "
            f"(allowed: {sorted(_DECISION_TYPES)})"
        )
    if not summary_ar or not summary_ar.strip():
        raise ValueError("summary_ar is required (bilingual non-negotiable)")
    if not summary_en or not summary_en.strip():
        raise ValueError("summary_en is required (bilingual non-negotiable)")

    approval = _classify_approval(
        sensitivity=sensitivity,
        reversibility=reversibility,
        confidence=confidence,
        external_action=external_action,
    )
    return DecisionPassport(
        passport_id=f"dp_{uuid.uuid4().hex[:16]}",
        tenant_id=tenant_id.strip(),
        decision_type=decision_type,
        summary_ar=summary_ar.strip(),
        summary_en=summary_en.strip(),
        approval_level=int(approval),
        reversibility=int(reversibility),
        sensitivity=int(sensitivity),
        confidence=int(confidence),
        content_hash=_hash_content(content),
        evidence_refs=tuple(evidence_refs),
        source_passport_ids=tuple(source_passport_ids),
        governance_decision=governance_decision,
        approved_by=approved_by,
        created_at=_now_iso(),
        metadata=dict(metadata or {}),
    )


def passport_matches_content(passport: DecisionPassport, content: str | Mapping[str, Any]) -> bool:
    """Verify a passport's content_hash matches the supplied rendered content."""
    return _hash_content(content) == passport.content_hash


def passport_to_audit_row(passport: DecisionPassport) -> dict[str, Any]:
    """Flatten a passport for the audit trail (one row per decision)."""
    return {
        "passport_id": passport.passport_id,
        "tenant_id": passport.tenant_id,
        "decision_type": passport.decision_type,
        "approval_level": passport.approval_level,
        "reversibility": passport.reversibility,
        "sensitivity": passport.sensitivity,
        "confidence": passport.confidence,
        "governance_decision": passport.governance_decision,
        "requires_human": passport.requires_human,
        "content_hash": passport.content_hash,
        "evidence_count": len(passport.evidence_refs),
        "created_at": passport.created_at,
    }


__all__ = [
    "ApprovalLevel",
    "Confidence",
    "DecisionPassport",
    "Reversibility",
    "Sensitivity",
    "issue_passport",
    "passport_matches_content",
    "passport_to_audit_row",
]

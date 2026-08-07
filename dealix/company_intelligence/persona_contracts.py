"""Canonical Persona contracts for Company Intelligence.

A Persona defines one tenant-scoped ideal customer profile (ICP) or
target buyer persona, grounded in evidence from signals, outcomes, and
learning events. Personas feed the Opportunity Graph and Proposal
generation — ensuring outreach and scoring are profile-driven.

The models are persistence-neutral: no database, network, or LLM calls.

Entity ownership: Persona → company_brain
    (company brain target-persona definitions).
Required fields: tenant_id, name, evidence.
Forbidden parallel names: ICPProfile, BuyerAvatar.
"""
from __future__ import annotations

import json
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

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class PersonaStatus(StrEnum):
    """Lifecycle states for a target persona."""

    DRAFT = "draft"
    ACTIVE = "active"
    UNDER_REVIEW = "under_review"
    RETIRED = "retired"


# ---------------------------------------------------------------------------
# Stable ID generation
# ---------------------------------------------------------------------------


def _stable_persona_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"persona_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Canonical Persona contract
# ---------------------------------------------------------------------------


class CanonicalPersona(BaseModel):
    """One tenant-scoped ideal customer profile or target buyer persona.

    Personas capture who Dealix (or a customer tenant) is targeting,
    grounded in evidence. They drive ICP scoring, opportunity
    prioritization, and outreach tone selection.

    Key invariants:
      - Name cannot be empty.
      - At least one evidence reference is required.
      - Persona ID is deterministic from tenant + name.
      - No unsupported market-leadership claims.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString
    persona_id: NonEmptyString

    # Persona details
    name: NonEmptyString
    description: str = ""

    # Targeting criteria
    target_sectors: tuple[str, ...] = ()
    target_regions: tuple[str, ...] = ()
    target_size_bands: tuple[str, ...] = ()
    pain_points: tuple[str, ...] = ()
    preferred_channels: tuple[str, ...] = ()

    # Status
    status: PersonaStatus = PersonaStatus.DRAFT

    # Scoring
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)

    # Evidence
    evidence_refs: tuple[str, ...] = ()

    # Provenance
    source_id: NonEmptyString

    @model_validator(mode="after")
    def enforce_persona_invariants(self) -> CanonicalPersona:
        # At least one evidence reference
        if len(self.evidence_refs) == 0:
            raise ValueError(
                "persona requires at least one evidence reference"
            )

        # Verify deterministic ID
        expected_id = _stable_persona_id({
            "name": self.name,
            "tenant_id": self.tenant_id,
        })
        if self.persona_id != expected_id:
            raise ValueError("persona_id does not match the canonical payload")

        return self


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------

_PERSONA_TRANSITIONS: dict[PersonaStatus, frozenset[PersonaStatus]] = {
    PersonaStatus.DRAFT: frozenset({PersonaStatus.ACTIVE, PersonaStatus.RETIRED}),
    PersonaStatus.ACTIVE: frozenset({PersonaStatus.UNDER_REVIEW, PersonaStatus.RETIRED}),
    PersonaStatus.UNDER_REVIEW: frozenset({PersonaStatus.ACTIVE, PersonaStatus.RETIRED}),
    PersonaStatus.RETIRED: frozenset(),  # terminal
}


def valid_persona_transitions_from(status: PersonaStatus) -> frozenset[PersonaStatus]:
    """Return the set of valid target states from *status*."""
    return _PERSONA_TRANSITIONS.get(status, frozenset())


def is_valid_persona_transition(
    from_status: PersonaStatus,
    to_status: PersonaStatus,
) -> bool:
    """Check whether *from_status* → *to_status* is a valid transition."""
    return to_status in valid_persona_transitions_from(from_status)


def transition_persona(
    persona: CanonicalPersona,
    *,
    to_status: PersonaStatus,
) -> CanonicalPersona:
    """Return a new CanonicalPersona with *to_status* applied.

    Raises ValueError on invalid transitions. The original is never mutated.
    """
    if not is_valid_persona_transition(persona.status, to_status):
        raise ValueError(
            f"invalid persona transition: {persona.status.value} → {to_status.value}"
        )
    updates: dict[str, Any] = {"status": to_status}
    return type(persona).model_validate({**persona.model_dump(), **updates})


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def build_persona(
    *,
    tenant_id: str,
    name: str,
    source_id: str,
    description: str = "",
    target_sectors: tuple[str, ...] = (),
    target_regions: tuple[str, ...] = (),
    target_size_bands: tuple[str, ...] = (),
    pain_points: tuple[str, ...] = (),
    preferred_channels: tuple[str, ...] = (),
    status: PersonaStatus = PersonaStatus.DRAFT,
    confidence: float = 0.5,
    evidence_refs: tuple[str, ...] = ("manual_observation",),
) -> CanonicalPersona:
    """Build a deterministic, evidence-grounded target persona."""

    persona_id = _stable_persona_id({
        "name": name.strip(),
        "tenant_id": tenant_id.strip(),
    })

    return CanonicalPersona(
        tenant_id=tenant_id,
        persona_id=persona_id,
        name=name,
        description=description,
        target_sectors=target_sectors,
        target_regions=target_regions,
        target_size_bands=target_size_bands,
        pain_points=pain_points,
        preferred_channels=preferred_channels,
        status=status,
        confidence=confidence,
        evidence_refs=evidence_refs,
        source_id=source_id,
    )

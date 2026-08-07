"""Canonical Offer contracts for Company Intelligence.

An Offer represents one tenant-scoped commercial offering in the Dealix
offer ladder. Offers flow through the Company Brain and Opportunity Graph
to become Proposals. The canonical contract normalizes the existing
ServiceOffering registry without replacing it.

The models are persistence-neutral: no database, network, or LLM calls.

Entity ownership: Offer → commercial_offers
    (canonical commercial offer ladder and quote-only constraints).
Required fields: tenant_id, name, status, approval_policy.
Forbidden parallel names: Package, ProductOffer.
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


class OfferStatus(StrEnum):
    """Commercial status of an offer in the ladder."""

    FREE_ENTRY = "free_entry"
    QUOTE_ONLY = "quote_only"
    PUBLIC_APPROVED = "public_approved"
    INTERNAL_EXPERIMENT = "internal_experiment"
    FUTURE = "future"
    RETIRED = "retired"


class OfferApprovalPolicy(StrEnum):
    """Approval policy governing how the offer can be sold."""

    SELF_SERVE = "self_serve"
    FOUNDER_APPROVAL = "founder_approval"
    DISCOVERY_FIRST = "discovery_first"
    BLOCKED = "blocked"


class OfferPriceUnit(StrEnum):
    """Unit type for offer pricing."""

    ONE_TIME = "one_time"
    PER_MONTH = "per_month"
    CUSTOM = "custom"


# ---------------------------------------------------------------------------
# Stable ID generation
# ---------------------------------------------------------------------------


def _stable_offer_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"offer_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Canonical Offer contract
# ---------------------------------------------------------------------------


class CanonicalOffer(BaseModel):
    """One tenant-scoped, normalized commercial offer.

    Offers are the building blocks of the Dealix commercial ladder. Each
    offer has a status and approval policy that control when and how it
    can be sold. Only `free_entry` and `quote_only` are commercially
    active unless separately approved.

    Key invariants:
      - A proposal is not an invoice; an invoice is not revenue.
      - Only free_entry and public_approved can have price_sar=0.
      - quote_only offers must use discovery_first approval.
      - internal_experiment and future offers must use blocked approval.
      - Offer ID is deterministic from tenant + offer_key.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString
    offer_id: NonEmptyString

    # Offer details
    offer_key: NonEmptyString
    name_ar: NonEmptyString
    name_en: NonEmptyString

    # Commercial
    status: OfferStatus
    approval_policy: OfferApprovalPolicy
    price_unit: OfferPriceUnit = OfferPriceUnit.ONE_TIME

    # Scoring
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)

    # Evidence
    evidence_refs: tuple[str, ...] = ()

    # Provenance
    source_id: NonEmptyString

    @model_validator(mode="after")
    def enforce_offer_invariants(self) -> CanonicalOffer:
        # quote_only must use discovery_first approval
        if (
            self.status == OfferStatus.QUOTE_ONLY
            and self.approval_policy != OfferApprovalPolicy.DISCOVERY_FIRST
        ):
            raise ValueError(
                "quote_only offers must use discovery_first approval policy"
            )

        # internal_experiment and future must use blocked approval
        if self.status in {
            OfferStatus.INTERNAL_EXPERIMENT,
            OfferStatus.FUTURE,
        } and self.approval_policy != OfferApprovalPolicy.BLOCKED:
            raise ValueError(
                "internal_experiment and future offers must use blocked approval policy"
            )

        # retired offers must use blocked approval
        if (
            self.status == OfferStatus.RETIRED
            and self.approval_policy != OfferApprovalPolicy.BLOCKED
        ):
            raise ValueError(
                "retired offers must use blocked approval policy"
            )

        # Verify deterministic ID
        expected_id = _stable_offer_id({
            "offer_key": self.offer_key,
            "tenant_id": self.tenant_id,
        })
        if self.offer_id != expected_id:
            raise ValueError("offer_id does not match the canonical payload")

        return self


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def build_offer(
    *,
    tenant_id: str,
    offer_key: str,
    name_ar: str,
    name_en: str,
    status: OfferStatus,
    approval_policy: OfferApprovalPolicy,
    source_id: str,
    price_unit: OfferPriceUnit = OfferPriceUnit.ONE_TIME,
    confidence: float = 0.5,
    evidence_refs: tuple[str, ...] = (),
) -> CanonicalOffer:
    """Build a deterministic, normalized commercial offer."""

    offer_id = _stable_offer_id({
        "offer_key": offer_key.strip(),
        "tenant_id": tenant_id.strip(),
    })

    return CanonicalOffer(
        tenant_id=tenant_id,
        offer_id=offer_id,
        offer_key=offer_key,
        name_ar=name_ar,
        name_en=name_en,
        status=status,
        approval_policy=approval_policy,
        source_id=source_id,
        price_unit=price_unit,
        confidence=confidence,
        evidence_refs=evidence_refs,
    )

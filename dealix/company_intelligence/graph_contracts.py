"""Canonical Company and Contact graph contracts for Company Intelligence.

These entities form the core of the opportunity graph — the
company/contact/signal graph that feeds every Company Loop. Companies and
Contacts are tenant-scoped, evidence-graded, and never authorize external
action by themselves.

The models are persistence-neutral: no database, network, or LLM calls.

Entity ownership:
  Company  → opportunity_graph (company/contact/signal graph)
  Contact  → opportunity_graph (company/contact/signal graph)

Forbidden parallel names:
  Company: Account, ProspectCompany, OrganizationRecord
  Contact: LeadPerson, ProspectContact
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

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class CompanyStatus(StrEnum):
    """Lifecycle states for a company in the graph."""

    DISCOVERED = "discovered"
    RESEARCHED = "researched"
    QUALIFIED = "qualified"
    ACTIVE = "active"
    CHURNED = "churned"
    PARKED = "parked"


class ContactRole(StrEnum):
    """Standard roles for contacts within a company."""

    FOUNDER = "founder"
    CEO = "ceo"
    GM = "gm"
    CTO = "cto"
    CFO = "cfo"
    VP_SALES = "vp_sales"
    VP_OPS = "vp_ops"
    SALES_LEAD = "sales_lead"
    OPS_LEAD = "ops_lead"
    CHAMPION = "champion"
    DECISION_MAKER = "decision_maker"
    INFLUENCER = "influencer"
    END_USER = "end_user"
    OTHER = "other"


class ContactStatus(StrEnum):
    """Lifecycle states for a contact in the graph."""

    IDENTIFIED = "identified"
    VERIFIED = "verified"
    ENGAGED = "engaged"
    INACTIVE = "inactive"
    OPTED_OUT = "opted_out"


class RelationshipStrength(StrEnum):
    """Strength of relationship between Dealix and the contact/company."""

    UNKNOWN = "unknown"
    COLD = "cold"
    WARM = "warm"
    ACTIVE = "active"
    STRONG = "strong"


# ---------------------------------------------------------------------------
# Stable ID generation (matches outcome_contracts / action_contracts pattern)
# ---------------------------------------------------------------------------


def _stable_company_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"company_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


def _stable_contact_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"contact_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Canonical Company contract
# ---------------------------------------------------------------------------


class CanonicalCompany(BaseModel):
    """One tenant-scoped, evidence-graded company in the opportunity graph.

    Companies are nodes in the company/contact/signal graph. They hold
    profile and classification data but never authorize external action
    by themselves — that requires the full Opportunity → Action → Approval
    chain.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString
    company_id: NonEmptyString
    deduplication_key: NonEmptyString

    # Profile
    name: NonEmptyString
    name_ar: str = ""
    sector: str = ""
    city: str = ""
    region: str = ""
    website: str = ""
    employee_count_estimate: int | None = None

    # Provenance
    source_id: NonEmptyString
    source_url: str = ""

    # Scoring
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)

    # Classification
    status: CompanyStatus = CompanyStatus.DISCOVERED
    relationship_strength: RelationshipStrength = RelationshipStrength.UNKNOWN
    icp_fit_score: float = Field(default=0.0, ge=0.0, le=1.0)

    # Context links
    signal_ids: tuple[str, ...] = ()
    opportunity_ids: tuple[str, ...] = ()

    # Timestamps
    discovered_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_enriched_at: datetime | None = None

    @model_validator(mode="after")
    def enforce_company_invariants(self) -> CanonicalCompany:
        # Verify deterministic ID
        expected_id = _stable_company_id({
            "deduplication_key": self.deduplication_key,
            "source_id": self.source_id,
            "tenant_id": self.tenant_id,
        })
        if self.company_id != expected_id:
            raise ValueError("company_id does not match the canonical payload")

        return self


# ---------------------------------------------------------------------------
# Canonical Contact contract
# ---------------------------------------------------------------------------


class CanonicalContact(BaseModel):
    """One tenant-scoped, evidence-graded contact in the opportunity graph.

    Contacts belong to a Company and carry their own consent posture.
    A Contact never authorizes external action by itself — contacting
    requires a Draft → Approval chain with lawful-contact-basis validation.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString
    contact_id: NonEmptyString
    deduplication_key: NonEmptyString

    # Profile
    name: str = ""
    name_ar: str = ""
    role: ContactRole = ContactRole.OTHER
    email: str = ""
    phone: str = ""

    # Ownership
    company_id: NonEmptyString

    # Provenance
    source_id: NonEmptyString

    # Scoring
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)

    # Classification
    status: ContactStatus = ContactStatus.IDENTIFIED
    relationship_strength: RelationshipStrength = RelationshipStrength.UNKNOWN
    consent_status: str = "unknown"
    consent_proof_ref: str = ""

    # Context links
    signal_ids: tuple[str, ...] = ()

    # Timestamps
    identified_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def enforce_contact_invariants(self) -> CanonicalContact:
        # Opted-out contacts cannot be engaged
        if self.consent_status == "opted_out" and self.status == ContactStatus.ENGAGED:
            raise ValueError(
                "opted-out contacts cannot be in engaged status"
            )

        # Verify deterministic ID
        expected_id = _stable_contact_id({
            "company_id": self.company_id,
            "deduplication_key": self.deduplication_key,
            "source_id": self.source_id,
            "tenant_id": self.tenant_id,
        })
        if self.contact_id != expected_id:
            raise ValueError("contact_id does not match the canonical payload")

        return self


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------


def build_company(
    *,
    tenant_id: str,
    deduplication_key: str,
    name: str,
    source_id: str,
    name_ar: str = "",
    sector: str = "",
    city: str = "",
    region: str = "",
    website: str = "",
    employee_count_estimate: int | None = None,
    source_url: str = "",
    confidence: float = 0.5,
    status: CompanyStatus = CompanyStatus.DISCOVERED,
    relationship_strength: RelationshipStrength = RelationshipStrength.UNKNOWN,
    icp_fit_score: float = 0.0,
    signal_ids: tuple[str, ...] = (),
    opportunity_ids: tuple[str, ...] = (),
    last_enriched_at: datetime | None = None,
) -> CanonicalCompany:
    """Build a deterministic, idempotent, evidence-graded company."""

    company_id = _stable_company_id({
        "deduplication_key": deduplication_key.strip(),
        "source_id": source_id.strip(),
        "tenant_id": tenant_id.strip(),
    })

    return CanonicalCompany(
        tenant_id=tenant_id,
        company_id=company_id,
        deduplication_key=deduplication_key,
        name=name,
        name_ar=name_ar,
        sector=sector,
        city=city,
        region=region,
        website=website,
        employee_count_estimate=employee_count_estimate,
        source_id=source_id,
        source_url=source_url,
        confidence=confidence,
        status=status,
        relationship_strength=relationship_strength,
        icp_fit_score=icp_fit_score,
        signal_ids=signal_ids,
        opportunity_ids=opportunity_ids,
        last_enriched_at=last_enriched_at,
    )


def build_contact(
    *,
    tenant_id: str,
    deduplication_key: str,
    company_id: str,
    source_id: str,
    name: str = "",
    name_ar: str = "",
    role: ContactRole = ContactRole.OTHER,
    email: str = "",
    phone: str = "",
    confidence: float = 0.5,
    status: ContactStatus = ContactStatus.IDENTIFIED,
    relationship_strength: RelationshipStrength = RelationshipStrength.UNKNOWN,
    consent_status: str = "unknown",
    consent_proof_ref: str = "",
    signal_ids: tuple[str, ...] = (),
) -> CanonicalContact:
    """Build a deterministic, idempotent, evidence-graded contact."""

    contact_id = _stable_contact_id({
        "company_id": company_id.strip(),
        "deduplication_key": deduplication_key.strip(),
        "source_id": source_id.strip(),
        "tenant_id": tenant_id.strip(),
    })

    return CanonicalContact(
        tenant_id=tenant_id,
        contact_id=contact_id,
        deduplication_key=deduplication_key,
        name=name,
        name_ar=name_ar,
        role=role,
        email=email,
        phone=phone,
        company_id=company_id,
        source_id=source_id,
        confidence=confidence,
        status=status,
        relationship_strength=relationship_strength,
        consent_status=consent_status,
        consent_proof_ref=consent_proof_ref,
        signal_ids=signal_ids,
    )

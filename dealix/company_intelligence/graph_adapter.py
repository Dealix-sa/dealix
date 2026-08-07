"""Fail-closed adapter from operational Lead to canonical Company and Contact truth.

Bridges ``auto_client_acquisition.agents.intake.Lead`` into
``CanonicalCompany`` and ``CanonicalContact`` without escalating authority.
A single Lead may produce both a Company (for the organization) and a Contact
(for the individual) — the two entities are linked via the canonical
``company_id``.

Key constraints:
  - The adapter never grants consent; ``consent_status`` starts as ``"unknown"``.
  - Company fit scores map from the Lead's ``fit_score`` but are clamped.
  - Employee count is parsed from ``company_size`` string if numeric.
  - Both entities are frozen, deterministic, and tenant-scoped.
  - The adapter requires either a company_name or contact_name — empty leads
    are rejected.
"""
from __future__ import annotations

from typing import Any

from dealix.company_intelligence.graph_contracts import (
    CanonicalCompany,
    CanonicalContact,
    CompanyStatus,
    ContactRole,
    RelationshipStrength,
    build_company,
    build_contact,
)


def _parse_employee_count(company_size: str | None) -> int | None:
    """Extract numeric employee estimate from string like '50', '20-200', etc."""
    if not company_size:
        return None
    # Strip non-numeric chars and take first number
    cleaned = company_size.strip().split("-")[0].split("–")[0].strip()
    # Remove common suffixes
    for suffix in ("+", " employees", " موظف"):
        cleaned = cleaned.replace(suffix, "")
    try:
        return int(cleaned)
    except (ValueError, TypeError):
        return None


def normalize_lead_to_company(
    lead: Any,
    *,
    tenant_id: str,
    source_id: str,
) -> CanonicalCompany:
    """Normalize the company aspect of a Lead into a ``CanonicalCompany``.

    Parameters
    ----------
    lead:
        A ``Lead`` or any duck-typed object with ``company_name``,
        optionally ``sector``, ``region``, ``company_size``, ``fit_score``,
        ``id``, and ``dedup_hash``.
    tenant_id:
        The tenant scope for the resulting canonical company.
    source_id:
        Source identity for provenance tracking.
    """
    company_name = str(getattr(lead, "company_name", "") or "").strip()
    if not company_name:
        raise ValueError("lead must have a non-empty company_name")

    # Deduplication key — use dedup_hash if available, else lead.id + company
    dedup_hash = str(getattr(lead, "dedup_hash", "") or "").strip()
    lead_id = str(getattr(lead, "id", "") or "").strip()
    deduplication_key = dedup_hash or f"lead:{lead_id}:{company_name}" if lead_id else company_name

    sector = str(getattr(lead, "sector", "") or "").strip()
    region = str(getattr(lead, "region", "") or "").strip()
    company_size = getattr(lead, "company_size", None)
    employee_count = _parse_employee_count(str(company_size) if company_size else None)

    fit_score = float(getattr(lead, "fit_score", 0.0) or 0.0)
    fit_score = max(0.0, min(1.0, fit_score))

    return build_company(
        tenant_id=tenant_id,
        deduplication_key=deduplication_key,
        name=company_name,
        source_id=source_id,
        sector=sector,
        region=region,
        employee_count_estimate=employee_count,
        confidence=0.5,
        status=CompanyStatus.DISCOVERED,
        relationship_strength=RelationshipStrength.COLD,
        icp_fit_score=fit_score,
    )


def normalize_lead_to_contact(
    lead: Any,
    *,
    tenant_id: str,
    source_id: str,
    company_id: str,
) -> CanonicalContact:
    """Normalize the contact aspect of a Lead into a ``CanonicalContact``.

    Parameters
    ----------
    lead:
        A ``Lead`` or any duck-typed object with ``contact_name``,
        optionally ``contact_email``, ``contact_phone``, ``id``,
        and ``dedup_hash``.
    tenant_id:
        The tenant scope for the resulting canonical contact.
    source_id:
        Source identity for provenance tracking.
    company_id:
        The canonical company_id linking this contact to its company.
    """
    contact_name = str(getattr(lead, "contact_name", "") or "").strip()
    if not contact_name:
        raise ValueError("lead must have a non-empty contact_name")

    # Deduplication key
    dedup_hash = str(getattr(lead, "dedup_hash", "") or "").strip()
    lead_id = str(getattr(lead, "id", "") or "").strip()
    deduplication_key = (
        f"contact:{dedup_hash}" if dedup_hash
        else f"contact:{lead_id}:{contact_name}" if lead_id
        else f"contact:{contact_name}"
    )

    email = str(getattr(lead, "contact_email", "") or "").strip()
    phone = str(getattr(lead, "contact_phone", "") or "").strip()

    return build_contact(
        tenant_id=tenant_id,
        deduplication_key=deduplication_key,
        company_id=company_id,
        name=contact_name,
        source_id=source_id,
        email=email,
        phone=phone,
        role=ContactRole.DECISION_MAKER,  # Leads typically target decision makers
        confidence=0.5,
        relationship_strength=RelationshipStrength.COLD,
        consent_status="unknown",  # fail-closed: never assume consent
    )

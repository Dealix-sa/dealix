"""Tests for the normalize_lead_to_company and normalize_lead_to_contact adapters.

Verifies that operational Lead records are correctly bridged to
CanonicalCompany and CanonicalContact without escalating authority.
"""
from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace

import pytest

from dealix.company_intelligence import (
    CanonicalCompany,
    CanonicalContact,
    CompanyStatus,
    ContactRole,
    ContactStatus,
    RelationshipStrength,
)
from dealix.company_intelligence.graph_adapter import (
    normalize_lead_to_company,
    normalize_lead_to_contact,
)


def _lead(**overrides: object) -> SimpleNamespace:
    """Build a duck-typed Lead-like object."""
    values: dict[str, object] = {
        "id": "lead-001",
        "source": "website_form",
        "company_name": "Acme Saudi",
        "contact_name": "Ahmed Al-Rashid",
        "contact_email": "ahmed@acme.sa",
        "contact_phone": "+966512345678",
        "contact_channel": "email",
        "sector": "B2B SaaS",
        "company_size": "50",
        "region": "Riyadh",
        "budget": 10000.0,
        "message": "Interested in diagnostic",
        "urgency_score": 0.7,
        "fit_score": 0.8,
        "status": "new",
        "pain_points": ["no CRM", "manual follow-up"],
        "locale": "ar",
        "created_at": datetime(2026, 8, 1, 12, 0, 0),
        "dedup_hash": "abc123",
    }
    values.update(overrides)
    return SimpleNamespace(**values)


# ---------------------------------------------------------------------------
# Company normalization
# ---------------------------------------------------------------------------


class TestNormalizeLeadToCompany:
    """Core company normalization behavior."""

    def test_produces_canonical_company(self) -> None:
        lead = _lead()
        company = normalize_lead_to_company(
            lead, tenant_id="tenant-a", source_id="website"
        )

        assert isinstance(company, CanonicalCompany)
        assert company.tenant_id == "tenant-a"
        assert company.name == "Acme Saudi"
        assert company.sector == "B2B SaaS"
        assert company.region == "Riyadh"
        assert company.source_id == "website"
        assert company.status == CompanyStatus.DISCOVERED
        assert company.relationship_strength == RelationshipStrength.COLD

    def test_employee_count_parsed_from_numeric_string(self) -> None:
        company = normalize_lead_to_company(
            _lead(company_size="50"), tenant_id="t", source_id="s"
        )
        assert company.employee_count_estimate == 50

    def test_employee_count_parsed_from_range(self) -> None:
        company = normalize_lead_to_company(
            _lead(company_size="20-200"), tenant_id="t", source_id="s"
        )
        assert company.employee_count_estimate == 20

    def test_employee_count_none_for_non_numeric(self) -> None:
        company = normalize_lead_to_company(
            _lead(company_size="small"), tenant_id="t", source_id="s"
        )
        assert company.employee_count_estimate is None

    def test_employee_count_none_when_missing(self) -> None:
        company = normalize_lead_to_company(
            _lead(company_size=None), tenant_id="t", source_id="s"
        )
        assert company.employee_count_estimate is None

    def test_fit_score_mapped_to_icp(self) -> None:
        company = normalize_lead_to_company(
            _lead(fit_score=0.85), tenant_id="t", source_id="s"
        )
        assert company.icp_fit_score == 0.85

    def test_fit_score_clamped(self) -> None:
        company = normalize_lead_to_company(
            _lead(fit_score=1.5), tenant_id="t", source_id="s"
        )
        assert company.icp_fit_score == 1.0

    def test_rejects_empty_company_name(self) -> None:
        with pytest.raises(ValueError, match="company_name"):
            normalize_lead_to_company(
                _lead(company_name=""), tenant_id="t", source_id="s"
            )

    def test_deterministic_id(self) -> None:
        lead = _lead()
        a = normalize_lead_to_company(lead, tenant_id="t", source_id="s")
        b = normalize_lead_to_company(lead, tenant_id="t", source_id="s")
        assert a.company_id == b.company_id

    def test_different_tenant_different_id(self) -> None:
        lead = _lead()
        a = normalize_lead_to_company(lead, tenant_id="t1", source_id="s")
        b = normalize_lead_to_company(lead, tenant_id="t2", source_id="s")
        assert a.company_id != b.company_id

    def test_frozen_immutability(self) -> None:
        company = normalize_lead_to_company(
            _lead(), tenant_id="t", source_id="s"
        )
        with pytest.raises(Exception):
            company.name = "tampered"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Contact normalization
# ---------------------------------------------------------------------------


class TestNormalizeLeadToContact:
    """Core contact normalization behavior."""

    def test_produces_canonical_contact(self) -> None:
        lead = _lead()
        company = normalize_lead_to_company(
            lead, tenant_id="tenant-a", source_id="website"
        )
        contact = normalize_lead_to_contact(
            lead, tenant_id="tenant-a", source_id="website",
            company_id=company.company_id,
        )

        assert isinstance(contact, CanonicalContact)
        assert contact.tenant_id == "tenant-a"
        assert contact.name == "Ahmed Al-Rashid"
        assert contact.email == "ahmed@acme.sa"
        assert contact.phone == "+966512345678"
        assert contact.company_id == company.company_id
        assert contact.role == ContactRole.DECISION_MAKER
        assert contact.status == ContactStatus.IDENTIFIED

    def test_consent_always_unknown(self) -> None:
        """Adapter never grants consent — requires explicit ConsentBasis."""
        contact = normalize_lead_to_contact(
            _lead(), tenant_id="t", source_id="s", company_id="co-1"
        )
        assert contact.consent_status == "unknown"

    def test_relationship_always_cold(self) -> None:
        contact = normalize_lead_to_contact(
            _lead(), tenant_id="t", source_id="s", company_id="co-1"
        )
        assert contact.relationship_strength == RelationshipStrength.COLD

    def test_rejects_empty_contact_name(self) -> None:
        with pytest.raises(ValueError, match="contact_name"):
            normalize_lead_to_contact(
                _lead(contact_name=""),
                tenant_id="t", source_id="s", company_id="co-1",
            )

    def test_handles_missing_email_and_phone(self) -> None:
        contact = normalize_lead_to_contact(
            _lead(contact_email=None, contact_phone=None),
            tenant_id="t", source_id="s", company_id="co-1",
        )
        assert contact.email == ""
        assert contact.phone == ""

    def test_deterministic_id(self) -> None:
        lead = _lead()
        a = normalize_lead_to_contact(
            lead, tenant_id="t", source_id="s", company_id="co-1"
        )
        b = normalize_lead_to_contact(
            lead, tenant_id="t", source_id="s", company_id="co-1"
        )
        assert a.contact_id == b.contact_id

    def test_different_company_different_id(self) -> None:
        lead = _lead()
        a = normalize_lead_to_contact(
            lead, tenant_id="t", source_id="s", company_id="co-1"
        )
        b = normalize_lead_to_contact(
            lead, tenant_id="t", source_id="s", company_id="co-2"
        )
        assert a.contact_id != b.contact_id

    def test_frozen_immutability(self) -> None:
        contact = normalize_lead_to_contact(
            _lead(), tenant_id="t", source_id="s", company_id="co-1"
        )
        with pytest.raises(Exception):
            contact.name = "tampered"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# End-to-end: Lead → Company + Contact
# ---------------------------------------------------------------------------


class TestLeadToGraphEndToEnd:
    """Verify company+contact pair from a single Lead."""

    def test_company_and_contact_linked(self) -> None:
        lead = _lead()
        company = normalize_lead_to_company(
            lead, tenant_id="t", source_id="website"
        )
        contact = normalize_lead_to_contact(
            lead, tenant_id="t", source_id="website",
            company_id=company.company_id,
        )
        assert contact.company_id == company.company_id
        assert company.tenant_id == contact.tenant_id

    def test_both_entities_are_frozen(self) -> None:
        lead = _lead()
        company = normalize_lead_to_company(
            lead, tenant_id="t", source_id="s"
        )
        contact = normalize_lead_to_contact(
            lead, tenant_id="t", source_id="s",
            company_id=company.company_id,
        )
        for entity in [company, contact]:
            with pytest.raises(Exception):
                entity.tenant_id = "tampered"  # type: ignore[misc]

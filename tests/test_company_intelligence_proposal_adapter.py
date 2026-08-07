"""Tests for the normalize_proposal adapter.

Verifies that operational distribution-OS Proposals are correctly
bridged to CanonicalProposal without escalating authority.
"""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from dealix.company_intelligence import (
    CanonicalProposal,
    ProposalStatus,
)
from dealix.company_intelligence.proposal_adapter import normalize_proposal


def _proposal(**overrides: object) -> SimpleNamespace:
    """Build a duck-typed Proposal-like object."""
    values: dict[str, object] = {
        "id": "prop_abc123",
        "prospect_id": "prospect-001",
        "product_id": "revenue_intelligence_sprint",
        "sector": "B2B SaaS",
        "problem": "No CRM, manual follow-up",
        "proposed_solution": "Revenue Intelligence Sprint for lead qualification",
        "scope": ["data quality", "account scoring", "draft pack"],
        "out_of_scope": ["no_scraping", "no_cold_whatsapp_automation"],
        "timeline": "7 days",
        "price_min_sar": 499,
        "price_max_sar": 499,
        "assumptions": ["founder access", "data available"],
        "evidence_level": 60,
        "risks": ["data quality unknown"],
        "payment_terms": "50% upfront, 50% on delivery",
        "next_step": "Schedule kickoff call",
        "approval_status": "pending_approval",
        "quality_issues": [],
        "created_at": "2026-08-05T12:00:00Z",
    }
    values.update(overrides)
    return SimpleNamespace(**values)


# ---------------------------------------------------------------------------
# Basic normalization
# ---------------------------------------------------------------------------


class TestNormalizeProposalBasic:
    """Core normalization behavior."""

    def test_produces_canonical_proposal(self) -> None:
        result = normalize_proposal(
            _proposal(),
            tenant_id="tenant-a",
            opportunity_id="opp-1",
            approval_id="approval-1",
        )
        assert isinstance(result, CanonicalProposal)
        assert result.tenant_id == "tenant-a"
        assert result.opportunity_id == "opp-1"
        assert result.approval_id == "approval-1"

    def test_offer_id_from_product_id(self) -> None:
        result = normalize_proposal(
            _proposal(product_id="my_product"),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert result.offer_id == "my_product"

    def test_company_id_from_prospect_id(self) -> None:
        result = normalize_proposal(
            _proposal(prospect_id="prospect-xyz"),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert result.company_id == "prospect-xyz"

    def test_frozen_immutability(self) -> None:
        result = normalize_proposal(
            _proposal(),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        with pytest.raises(Exception):
            result.status = ProposalStatus.SENT  # type: ignore[misc]

    def test_source_id_default(self) -> None:
        result = normalize_proposal(
            _proposal(),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert result.source_id == "distribution_os"

    def test_source_id_override(self) -> None:
        result = normalize_proposal(
            _proposal(),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
            source_id="sales_os",
        )
        assert result.source_id == "sales_os"


# ---------------------------------------------------------------------------
# Status mapping
# ---------------------------------------------------------------------------


class TestStatusMapping:
    """Verify approval status → ProposalStatus mapping."""

    @pytest.mark.parametrize(
        ("raw_status", "expected"),
        [
            ("pending_approval", ProposalStatus.PENDING_REVIEW),
            ("approved", ProposalStatus.APPROVED),
            ("rejected", ProposalStatus.REJECTED),
            # "sent" → APPROVED: adapter never escalates to SENT (requires
            # controlled execution with sent_at evidence)
            ("sent", ProposalStatus.APPROVED),
            ("draft", ProposalStatus.DRAFT),
            ("pending_review", ProposalStatus.PENDING_REVIEW),
            ("accepted", ProposalStatus.ACCEPTED),
            ("expired", ProposalStatus.EXPIRED),
            ("withdrawn", ProposalStatus.WITHDRAWN),
        ],
    )
    def test_status_mapping(
        self, raw_status: str, expected: ProposalStatus
    ) -> None:
        result = normalize_proposal(
            _proposal(approval_status=raw_status),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert result.status == expected

    def test_unknown_status_fails_closed_to_draft(self) -> None:
        result = normalize_proposal(
            _proposal(approval_status="finalized"),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert result.status == ProposalStatus.DRAFT

    def test_case_insensitive(self) -> None:
        result = normalize_proposal(
            _proposal(approval_status="PENDING_APPROVAL"),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert result.status == ProposalStatus.PENDING_REVIEW


# ---------------------------------------------------------------------------
# Confidence from evidence level
# ---------------------------------------------------------------------------


class TestConfidence:
    """Verify evidence_level → confidence normalization."""

    def test_evidence_level_60_gives_0_6(self) -> None:
        result = normalize_proposal(
            _proposal(evidence_level=60),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert result.confidence == pytest.approx(0.6)

    def test_evidence_level_0_gives_0(self) -> None:
        result = normalize_proposal(
            _proposal(evidence_level=0),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert result.confidence == 0.0

    def test_evidence_level_100_gives_1(self) -> None:
        result = normalize_proposal(
            _proposal(evidence_level=100),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert result.confidence == 1.0

    def test_evidence_level_clamped_above_100(self) -> None:
        result = normalize_proposal(
            _proposal(evidence_level=150),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert result.confidence == 1.0

    def test_evidence_level_negative_clamped(self) -> None:
        result = normalize_proposal(
            _proposal(evidence_level=-10),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert result.confidence == 0.0


# ---------------------------------------------------------------------------
# Content summary
# ---------------------------------------------------------------------------


class TestContentSummary:
    """Verify content summary composition."""

    def test_includes_problem(self) -> None:
        result = normalize_proposal(
            _proposal(problem="No CRM system"),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert "No CRM system" in result.content_summary

    def test_includes_solution(self) -> None:
        result = normalize_proposal(
            _proposal(proposed_solution="Revenue Sprint"),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert "Revenue Sprint" in result.content_summary

    def test_includes_scope(self) -> None:
        result = normalize_proposal(
            _proposal(scope=["data quality", "account scoring"]),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert "data quality" in result.content_summary

    def test_includes_timeline(self) -> None:
        result = normalize_proposal(
            _proposal(timeline="7 days"),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert "7 days" in result.content_summary

    def test_empty_fields_excluded(self) -> None:
        result = normalize_proposal(
            _proposal(problem="", proposed_solution="", scope=[], timeline=""),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert "Problem:" not in result.content_summary


# ---------------------------------------------------------------------------
# Pricing note
# ---------------------------------------------------------------------------


class TestPricingNote:
    """Verify pricing note composition."""

    def test_single_price(self) -> None:
        result = normalize_proposal(
            _proposal(price_min_sar=499, price_max_sar=499),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert "499 SAR" in result.pricing_note

    def test_price_range(self) -> None:
        result = normalize_proposal(
            _proposal(price_min_sar=499, price_max_sar=999),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert "499" in result.pricing_note
        assert "999" in result.pricing_note

    def test_includes_payment_terms(self) -> None:
        result = normalize_proposal(
            _proposal(payment_terms="50% upfront"),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert "50% upfront" in result.pricing_note

    def test_zero_prices_no_amount(self) -> None:
        result = normalize_proposal(
            _proposal(price_min_sar=0, price_max_sar=0, payment_terms=""),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert result.pricing_note == ""


# ---------------------------------------------------------------------------
# Evidence refs
# ---------------------------------------------------------------------------


class TestEvidenceRefs:
    """Verify evidence references from quality issues and risks."""

    def test_quality_issues_mapped(self) -> None:
        result = normalize_proposal(
            _proposal(quality_issues=["tone_too_aggressive"]),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert "quality:tone_too_aggressive" in result.evidence_refs

    def test_risks_mapped(self) -> None:
        result = normalize_proposal(
            _proposal(risks=["data quality unknown"]),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert "risk:data quality unknown" in result.evidence_refs

    def test_empty_issues_no_refs(self) -> None:
        result = normalize_proposal(
            _proposal(quality_issues=[], risks=[]),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert len(result.evidence_refs) == 0


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------


class TestDeterminism:
    """Verify deterministic proposal_id generation."""

    def test_same_inputs_same_id(self) -> None:
        a = normalize_proposal(
            _proposal(), tenant_id="t", opportunity_id="o", approval_id="a"
        )
        b = normalize_proposal(
            _proposal(), tenant_id="t", opportunity_id="o", approval_id="a"
        )
        assert a.proposal_id == b.proposal_id

    def test_different_tenant_different_id(self) -> None:
        a = normalize_proposal(
            _proposal(), tenant_id="t1", opportunity_id="o", approval_id="a"
        )
        b = normalize_proposal(
            _proposal(), tenant_id="t2", opportunity_id="o", approval_id="a"
        )
        assert a.proposal_id != b.proposal_id

    def test_different_version_different_id(self) -> None:
        a = normalize_proposal(
            _proposal(), tenant_id="t", opportunity_id="o", approval_id="a", version=1
        )
        b = normalize_proposal(
            _proposal(), tenant_id="t", opportunity_id="o", approval_id="a", version=2
        )
        assert a.proposal_id != b.proposal_id


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


class TestValidation:
    """Verify input validation."""

    def test_rejects_empty_product_id(self) -> None:
        with pytest.raises(ValueError, match="product_id"):
            normalize_proposal(
                _proposal(product_id=""),
                tenant_id="t",
                opportunity_id="o",
                approval_id="a",
            )

    def test_accepts_empty_prospect_id(self) -> None:
        """prospect_id is optional — maps to company_id which defaults to empty."""
        result = normalize_proposal(
            _proposal(prospect_id=""),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert result.company_id == ""

    def test_version_default_is_1(self) -> None:
        result = normalize_proposal(
            _proposal(),
            tenant_id="t",
            opportunity_id="o",
            approval_id="a",
        )
        assert result.version == 1

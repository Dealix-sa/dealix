"""Tests for the canonical Offer contracts.

Covers:
  - Deterministic ID generation and idempotency
  - Confidence scoring bounds
  - Status and approval policy invariants
  - Fail-closed on invalid inputs
  - Builder convenience
  - Entity ownership registry alignment
  - Frozen immutability
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.offer_contracts import (
    CanonicalOffer,
    OfferApprovalPolicy,
    OfferPriceUnit,
    OfferStatus,
    build_offer,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _offer(**overrides: object) -> CanonicalOffer:
    """Build a minimal valid offer, overriding any fields."""
    defaults: dict[str, object] = dict(
        tenant_id="tenant-a",
        offer_key="free_mini_diagnostic",
        name_ar="التشخيص المجاني المختصر",
        name_en="Free Mini Diagnostic",
        status=OfferStatus.FREE_ENTRY,
        approval_policy=OfferApprovalPolicy.SELF_SERVE,
        source_id="source-1",
    )
    defaults.update(overrides)
    return build_offer(**defaults)


# ---------------------------------------------------------------------------
# Deterministic identity
# ---------------------------------------------------------------------------


class TestDeterministicIdentity:
    def test_same_inputs_produce_same_id(self) -> None:
        a = _offer()
        b = _offer()
        assert a.offer_id == b.offer_id

    def test_different_offer_key_produces_different_id(self) -> None:
        a = _offer(offer_key="free_mini_diagnostic")
        b = _offer(offer_key="revenue_command_pilot_30d")
        assert a.offer_id != b.offer_id

    def test_different_tenant_produces_different_id(self) -> None:
        a = _offer(tenant_id="tenant-a")
        b = _offer(tenant_id="tenant-b")
        assert a.offer_id != b.offer_id

    def test_offer_id_format(self) -> None:
        a = _offer()
        assert a.offer_id.startswith("offer_")
        assert len(a.offer_id) == 6 + 16  # "offer_" + 16 hex chars

    def test_whitespace_in_offer_key_is_stripped(self) -> None:
        a = _offer(offer_key="  free_mini_diagnostic  ")
        b = _offer(offer_key="free_mini_diagnostic")
        assert a.offer_id == b.offer_id

    def test_status_does_not_affect_id(self) -> None:
        """Status is mutable metadata — it must not affect the stable ID."""
        a = _offer(
            status=OfferStatus.FREE_ENTRY,
            approval_policy=OfferApprovalPolicy.SELF_SERVE,
        )
        b = _offer(
            status=OfferStatus.PUBLIC_APPROVED,
            approval_policy=OfferApprovalPolicy.FOUNDER_APPROVAL,
        )
        assert a.offer_id == b.offer_id


# ---------------------------------------------------------------------------
# Confidence scoring
# ---------------------------------------------------------------------------


class TestConfidenceScoring:
    def test_default_confidence(self) -> None:
        a = _offer()
        assert a.confidence == 0.5

    def test_confidence_above_one_rejected(self) -> None:
        with pytest.raises(ValueError):
            _offer(confidence=1.5)

    def test_confidence_below_zero_rejected(self) -> None:
        with pytest.raises(ValueError):
            _offer(confidence=-0.1)

    def test_confidence_at_boundaries(self) -> None:
        a = _offer(confidence=0.0)
        assert a.confidence == 0.0
        b = _offer(confidence=1.0)
        assert b.confidence == 1.0


# ---------------------------------------------------------------------------
# Status and approval invariants
# ---------------------------------------------------------------------------


class TestStatusApprovalInvariants:
    def test_quote_only_requires_discovery_first(self) -> None:
        with pytest.raises(ValueError, match="discovery_first"):
            _offer(
                status=OfferStatus.QUOTE_ONLY,
                approval_policy=OfferApprovalPolicy.SELF_SERVE,
            )

    def test_quote_only_with_discovery_first_accepted(self) -> None:
        a = _offer(
            status=OfferStatus.QUOTE_ONLY,
            approval_policy=OfferApprovalPolicy.DISCOVERY_FIRST,
        )
        assert a.status == OfferStatus.QUOTE_ONLY
        assert a.approval_policy == OfferApprovalPolicy.DISCOVERY_FIRST

    def test_internal_experiment_requires_blocked(self) -> None:
        with pytest.raises(ValueError, match="blocked"):
            _offer(
                status=OfferStatus.INTERNAL_EXPERIMENT,
                approval_policy=OfferApprovalPolicy.SELF_SERVE,
            )

    def test_internal_experiment_with_blocked_accepted(self) -> None:
        a = _offer(
            status=OfferStatus.INTERNAL_EXPERIMENT,
            approval_policy=OfferApprovalPolicy.BLOCKED,
        )
        assert a.status == OfferStatus.INTERNAL_EXPERIMENT

    def test_future_requires_blocked(self) -> None:
        with pytest.raises(ValueError, match="blocked"):
            _offer(
                status=OfferStatus.FUTURE,
                approval_policy=OfferApprovalPolicy.FOUNDER_APPROVAL,
            )

    def test_future_with_blocked_accepted(self) -> None:
        a = _offer(
            status=OfferStatus.FUTURE,
            approval_policy=OfferApprovalPolicy.BLOCKED,
        )
        assert a.status == OfferStatus.FUTURE

    def test_retired_requires_blocked(self) -> None:
        with pytest.raises(ValueError, match="blocked"):
            _offer(
                status=OfferStatus.RETIRED,
                approval_policy=OfferApprovalPolicy.SELF_SERVE,
            )

    def test_retired_with_blocked_accepted(self) -> None:
        a = _offer(
            status=OfferStatus.RETIRED,
            approval_policy=OfferApprovalPolicy.BLOCKED,
        )
        assert a.status == OfferStatus.RETIRED

    def test_free_entry_allows_self_serve(self) -> None:
        a = _offer(
            status=OfferStatus.FREE_ENTRY,
            approval_policy=OfferApprovalPolicy.SELF_SERVE,
        )
        assert a.approval_policy == OfferApprovalPolicy.SELF_SERVE

    def test_public_approved_allows_founder_approval(self) -> None:
        a = _offer(
            status=OfferStatus.PUBLIC_APPROVED,
            approval_policy=OfferApprovalPolicy.FOUNDER_APPROVAL,
        )
        assert a.approval_policy == OfferApprovalPolicy.FOUNDER_APPROVAL


# ---------------------------------------------------------------------------
# Extra field protection
# ---------------------------------------------------------------------------


class TestExtraFieldProtection:
    def test_extra_fields_forbidden(self) -> None:
        a = _offer()
        data = a.model_dump()
        data["rogue_field"] = "injected"
        with pytest.raises(ValueError):
            CanonicalOffer(**data)


# ---------------------------------------------------------------------------
# Builder defaults
# ---------------------------------------------------------------------------


class TestBuilderDefaults:
    def test_default_confidence(self) -> None:
        a = _offer()
        assert a.confidence == 0.5

    def test_default_price_unit(self) -> None:
        a = _offer()
        assert a.price_unit == OfferPriceUnit.ONE_TIME

    def test_default_evidence_empty(self) -> None:
        a = _offer()
        assert a.evidence_refs == ()

    def test_builder_with_full_context(self) -> None:
        a = build_offer(
            tenant_id="tenant-a",
            offer_key="revenue_command_pilot_30d",
            name_ar="تجربة مركز قيادة الإيرادات — 30 يومًا",
            name_en="Revenue Command Pilot — 30 days",
            status=OfferStatus.QUOTE_ONLY,
            approval_policy=OfferApprovalPolicy.DISCOVERY_FIRST,
            source_id="service-catalog-registry",
            price_unit=OfferPriceUnit.CUSTOM,
            confidence=0.9,
            evidence_refs=("catalog-entry", "founder-approval"),
        )
        assert a.status == OfferStatus.QUOTE_ONLY
        assert a.approval_policy == OfferApprovalPolicy.DISCOVERY_FIRST
        assert a.price_unit == OfferPriceUnit.CUSTOM
        assert a.confidence == 0.9
        assert len(a.evidence_refs) == 2


# ---------------------------------------------------------------------------
# Frozen immutability
# ---------------------------------------------------------------------------


class TestFrozenImmutability:
    def test_offer_is_frozen(self) -> None:
        a = _offer()
        with pytest.raises(Exception):
            a.status = OfferStatus.RETIRED  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Entity ownership registry alignment
# ---------------------------------------------------------------------------


class TestEntityOwnershipAlignment:
    """Verify the contract satisfies the required fields from
    company_intelligence_entity_ownership.json for Offer."""

    def test_required_fields_present(self) -> None:
        a = _offer()
        # Required: tenant_id, name, status, approval_policy
        assert hasattr(a, "tenant_id") and a.tenant_id
        assert hasattr(a, "name_en") and a.name_en
        assert hasattr(a, "name_ar") and a.name_ar
        assert hasattr(a, "status") and a.status
        assert hasattr(a, "approval_policy") and a.approval_policy

    def test_empty_tenant_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_offer(
                tenant_id="",
                offer_key="test",
                name_ar="اختبار",
                name_en="Test",
                status=OfferStatus.FREE_ENTRY,
                approval_policy=OfferApprovalPolicy.SELF_SERVE,
                source_id="source-1",
            )

    def test_empty_offer_key_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_offer(
                tenant_id="tenant-a",
                offer_key="",
                name_ar="اختبار",
                name_en="Test",
                status=OfferStatus.FREE_ENTRY,
                approval_policy=OfferApprovalPolicy.SELF_SERVE,
                source_id="source-1",
            )

    def test_empty_name_ar_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_offer(
                tenant_id="tenant-a",
                offer_key="test",
                name_ar="",
                name_en="Test",
                status=OfferStatus.FREE_ENTRY,
                approval_policy=OfferApprovalPolicy.SELF_SERVE,
                source_id="source-1",
            )

    def test_empty_source_id_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_offer(
                tenant_id="tenant-a",
                offer_key="test",
                name_ar="اختبار",
                name_en="Test",
                status=OfferStatus.FREE_ENTRY,
                approval_policy=OfferApprovalPolicy.SELF_SERVE,
                source_id="",
            )

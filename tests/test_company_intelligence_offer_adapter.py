"""Tests for the ServiceOffering → CanonicalOffer adapter.

Covers:
  - Normalization of the active catalog entries
  - Status and approval policy mapping
  - Price unit mapping
  - Full catalog normalization
  - Evidence and provenance
"""
from __future__ import annotations

from dealix.company_intelligence.offer_adapter import (
    normalize_catalog,
    normalize_service_offering,
)
from dealix.company_intelligence.offer_contracts import (
    OfferApprovalPolicy,
    OfferPriceUnit,
    OfferStatus,
)

# ---------------------------------------------------------------------------
# Individual offering normalization
# ---------------------------------------------------------------------------


class TestNormalizeServiceOffering:
    def test_free_diagnostic(self) -> None:
        from auto_client_acquisition.service_catalog.registry import OFFERINGS

        free = next(o for o in OFFERINGS if o.id == "free_mini_diagnostic")
        offer = normalize_service_offering(free)
        assert offer.offer_key == "free_mini_diagnostic"
        assert offer.status == OfferStatus.FREE_ENTRY
        assert offer.approval_policy == OfferApprovalPolicy.SELF_SERVE
        assert offer.name_ar == free.name_ar
        assert offer.name_en == free.name_en

    def test_revenue_command_pilot(self) -> None:
        from auto_client_acquisition.service_catalog.registry import OFFERINGS

        pilot = next(o for o in OFFERINGS if o.id == "revenue_command_pilot_30d")
        offer = normalize_service_offering(pilot)
        assert offer.offer_key == "revenue_command_pilot_30d"
        assert offer.status == OfferStatus.QUOTE_ONLY
        assert offer.approval_policy == OfferApprovalPolicy.DISCOVERY_FIRST

    def test_internal_experiment_gets_blocked(self) -> None:
        from auto_client_acquisition.service_catalog.registry import OFFERINGS

        experiment = next(
            o for o in OFFERINGS
            if o.commercial_status == "internal_experiment"
        )
        offer = normalize_service_offering(experiment)
        assert offer.status == OfferStatus.INTERNAL_EXPERIMENT
        assert offer.approval_policy == OfferApprovalPolicy.BLOCKED

    def test_tenant_id_propagated(self) -> None:
        from auto_client_acquisition.service_catalog.registry import OFFERINGS

        offer = normalize_service_offering(OFFERINGS[0], tenant_id="customer-x")
        assert offer.tenant_id == "customer-x"

    def test_evidence_and_source(self) -> None:
        from auto_client_acquisition.service_catalog.registry import OFFERINGS

        offer = normalize_service_offering(OFFERINGS[0])
        assert offer.source_id == "auto_client_acquisition.service_catalog.registry"
        assert offer.evidence_refs == ("service-catalog-registry",)
        assert offer.confidence == 1.0


# ---------------------------------------------------------------------------
# Price unit mapping
# ---------------------------------------------------------------------------


class TestPriceUnitMapping:
    def test_one_time_mapping(self) -> None:
        from auto_client_acquisition.service_catalog.registry import OFFERINGS

        # Free diagnostic is one_time
        free = next(o for o in OFFERINGS if o.id == "free_mini_diagnostic")
        offer = normalize_service_offering(free)
        assert offer.price_unit == OfferPriceUnit.ONE_TIME

    def test_custom_mapping(self) -> None:
        from auto_client_acquisition.service_catalog.registry import OFFERINGS

        pilot = next(o for o in OFFERINGS if o.id == "revenue_command_pilot_30d")
        offer = normalize_service_offering(pilot)
        assert offer.price_unit == OfferPriceUnit.CUSTOM


# ---------------------------------------------------------------------------
# Full catalog normalization
# ---------------------------------------------------------------------------


class TestNormalizeCatalog:
    def test_catalog_produces_offers(self) -> None:
        offers = normalize_catalog()
        assert len(offers) > 0

    def test_all_offers_have_unique_ids(self) -> None:
        offers = normalize_catalog()
        ids = [o.offer_id for o in offers]
        assert len(ids) == len(set(ids))

    def test_all_offers_frozen(self) -> None:
        import pytest

        offers = normalize_catalog()
        for offer in offers:
            with pytest.raises(Exception):
                offer.status = OfferStatus.RETIRED  # type: ignore[misc]

    def test_commercially_active_count(self) -> None:
        """Only two offers should be commercially active."""
        offers = normalize_catalog()
        active = [
            o for o in offers
            if o.status in {OfferStatus.FREE_ENTRY, OfferStatus.QUOTE_ONLY}
        ]
        assert len(active) == 2

    def test_catalog_idempotent(self) -> None:
        a = normalize_catalog()
        b = normalize_catalog()
        assert [o.offer_id for o in a] == [o.offer_id for o in b]

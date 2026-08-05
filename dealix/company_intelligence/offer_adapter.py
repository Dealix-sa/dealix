"""Adapter: ServiceOffering registry → CanonicalOffer contracts.

Normalizes the existing service-catalog registry entries into the
canonical CanonicalOffer format without replacing the authoritative
ServiceOffering definitions. The adapter is the thin bridge between
the commercial catalog and the Company Intelligence contract layer.

No database, network, or LLM calls.
"""
from __future__ import annotations

from auto_client_acquisition.service_catalog.schemas import ServiceOffering

from dealix.company_intelligence.offer_contracts import (
    CanonicalOffer,
    OfferApprovalPolicy,
    OfferPriceUnit,
    OfferStatus,
    build_offer,
)


def _map_commercial_status(status: str) -> OfferStatus:
    """Map ServiceOffering commercial_status to CanonicalOffer OfferStatus."""
    mapping = {
        "free_entry": OfferStatus.FREE_ENTRY,
        "quote_only": OfferStatus.QUOTE_ONLY,
        "public_approved": OfferStatus.PUBLIC_APPROVED,
        "internal_experiment": OfferStatus.INTERNAL_EXPERIMENT,
        "future": OfferStatus.FUTURE,
    }
    return mapping.get(status, OfferStatus.INTERNAL_EXPERIMENT)


def _map_approval_policy(status: OfferStatus) -> OfferApprovalPolicy:
    """Derive approval policy from offer status per commercial rules."""
    if status == OfferStatus.FREE_ENTRY:
        return OfferApprovalPolicy.SELF_SERVE
    if status == OfferStatus.QUOTE_ONLY:
        return OfferApprovalPolicy.DISCOVERY_FIRST
    if status == OfferStatus.PUBLIC_APPROVED:
        return OfferApprovalPolicy.FOUNDER_APPROVAL
    # internal_experiment, future, retired → blocked
    return OfferApprovalPolicy.BLOCKED


def _map_price_unit(unit: str) -> OfferPriceUnit:
    """Map ServiceOffering price_unit to CanonicalOffer OfferPriceUnit."""
    mapping = {
        "one_time": OfferPriceUnit.ONE_TIME,
        "per_month": OfferPriceUnit.PER_MONTH,
        "custom": OfferPriceUnit.CUSTOM,
    }
    return mapping.get(unit, OfferPriceUnit.ONE_TIME)


def normalize_service_offering(
    offering: ServiceOffering,
    *,
    tenant_id: str = "dealix",
) -> CanonicalOffer:
    """Convert a ServiceOffering into a CanonicalOffer.

    The ServiceOffering remains the authoritative definition. This adapter
    creates a read-only normalized snapshot for the Company Intelligence
    contract layer.
    """
    offer_status = _map_commercial_status(offering.commercial_status)
    approval_policy = _map_approval_policy(offer_status)
    price_unit = _map_price_unit(offering.price_unit)

    return build_offer(
        tenant_id=tenant_id,
        offer_key=offering.id,
        name_ar=offering.name_ar,
        name_en=offering.name_en,
        status=offer_status,
        approval_policy=approval_policy,
        source_id="auto_client_acquisition.service_catalog.registry",
        price_unit=price_unit,
        confidence=1.0,
        evidence_refs=("service-catalog-registry",),
    )


def normalize_catalog(
    *,
    tenant_id: str = "dealix",
) -> list[CanonicalOffer]:
    """Normalize the full service catalog into CanonicalOffer contracts.

    Imports the catalog lazily to avoid circular dependencies.
    """
    from auto_client_acquisition.service_catalog.registry import OFFERINGS

    return [
        normalize_service_offering(offering, tenant_id=tenant_id)
        for offering in OFFERINGS
    ]

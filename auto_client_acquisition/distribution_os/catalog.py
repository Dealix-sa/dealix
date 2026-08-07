"""Commercial catalog surface for the Revenue Execution OS.

The single source of truth for products and prices is the EXISTING catalog —
``autonomous_growth.product_catalog`` (the five-rung ladder) plus the
higher-touch RevOps packages documented in
``docs/commercial/DEALIX_REVOPS_PACKAGES_AR.md``. This module does NOT invent
new products or prices; it provides lookup + ladder helpers over the existing
catalog so every draft / proposal / payment handoff links to a real product.
"""

from __future__ import annotations

from autonomous_growth.product_catalog import PRODUCT_CATALOG, Product, ProductTier

# Ordered ladder (rung 0 → rung 4). Upsell moves one rung up the tuple.
LADDER: tuple[ProductTier, ...] = (
    ProductTier.FREE_DIAGNOSTIC,
    ProductTier.SPRINT,
    ProductTier.DATA_PACK,
    ProductTier.MANAGED_OPS,
    ProductTier.CUSTOM_AI,
)


def all_products() -> list[Product]:
    """All catalog products, in ladder order."""
    return [PRODUCT_CATALOG[tier] for tier in LADDER]


def product_by_id(product_id: str) -> Product | None:
    for product in PRODUCT_CATALOG.values():
        if product.id == product_id:
            return product
    return None


def product_by_tier(tier: ProductTier | str) -> Product | None:
    if isinstance(tier, str):
        try:
            tier = ProductTier(tier)
        except ValueError:
            return None
    return PRODUCT_CATALOG.get(tier)


def is_valid_product_id(product_id: str) -> bool:
    return product_by_id(product_id) is not None


def price_band(product_id: str) -> tuple[int, int]:
    """Return ``(min_sar, max_sar)`` from the catalog. Raises on unknown id.

    Pricing is never invented here — it is read from the existing catalog.
    """
    product = product_by_id(product_id)
    if product is None:
        raise KeyError(f"unknown_product_id:{product_id}")
    high = product.price_max_sar or product.price_sar
    return (product.price_sar, high)


def next_rung(product_id: str) -> Product | None:
    """The next product up the ladder (the natural upsell), or ``None`` at top."""
    product = product_by_id(product_id)
    if product is None:
        return None
    idx = LADDER.index(product.tier)
    if idx + 1 >= len(LADDER):
        return None
    return PRODUCT_CATALOG[LADDER[idx + 1]]


def ladder_summary() -> list[dict[str, object]]:
    """Lightweight, serialisable ladder view for reports / API."""
    summary: list[dict[str, object]] = []
    for rung, tier in enumerate(LADDER):
        product = PRODUCT_CATALOG[tier]
        summary.append(
            {
                "rung": rung,
                "id": product.id,
                "tier": tier.value,
                "name_ar": product.name_ar,
                "name_en": product.name_en,
                "price_min_sar": product.price_sar,
                "price_max_sar": product.price_max_sar or product.price_sar,
                "delivery_days": product.delivery_days,
                "min_icp_score": product.min_icp_score,
            }
        )
    return summary


__all__ = [
    "LADDER",
    "Product",
    "ProductTier",
    "all_products",
    "is_valid_product_id",
    "ladder_summary",
    "next_rung",
    "price_band",
    "product_by_id",
    "product_by_tier",
]

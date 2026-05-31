"""
Hermes Products — Offer Registry + Product Readiness Gate.

كل offer يُمثَّل ككائن بيانات (Section 48) مع شروط جاهزية صارمة قبل
السماح بتسويقه أو بيعه (Section 49).
"""

from .offer_registry import (
    DEFAULT_OFFERS,
    Offer,
    OfferRegistry,
    OfferStatus,
    default_registry,
)
from .readiness_gate import ProductReadinessGate, ReadinessResult

__all__ = [
    "DEFAULT_OFFERS",
    "Offer",
    "OfferRegistry",
    "OfferStatus",
    "ProductReadinessGate",
    "ReadinessResult",
    "default_registry",
]

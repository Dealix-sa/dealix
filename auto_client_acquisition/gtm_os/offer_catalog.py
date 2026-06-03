"""Canonical operational offer ids for the Market Production OS.

This is the single source of truth for *which offer id a draft may reference*
so the quality gate can enforce ``offer_matched``. It is intentionally a thin
operational list — authoritative **pricing, scope, and packaging live in docs**
(`docs/OFFER_LADDER_AND_PRICING.md`, `docs/commercial/`) and must not be
invented or finalized in code. The five-rung ladder is the source of truth;
``ai_governance_review`` is the slow-track enterprise entry.
"""

from __future__ import annotations

# id -> (Arabic label, English label). Mirrors the governed five-rung ladder.
CATALOG_OFFERS: dict[str, tuple[str, str]] = {
    "free_diagnostic": ("تشخيص عمليات الذكاء (مجاني)", "Free AI Ops Diagnostic"),
    "revenue_intelligence_sprint": (
        "سبرنت ذكاء الإيرادات (7 أيام)",
        "7-Day Revenue Intelligence Sprint",
    ),
    "data_to_revenue_pack": ("حزمة البيانات إلى إيراد", "Data-to-Revenue Pack"),
    "managed_revenue_ops": ("تشغيل إيرادات مُدار", "Managed Revenue Ops"),
    "custom_ai_setup": ("تهيئة ذكاء مخصّص", "Custom AI Service Setup"),
    "ai_governance_review": ("مراجعة حوكمة الذكاء", "AI Governance Review"),
}

CATALOG_OFFER_IDS: frozenset[str] = frozenset(CATALOG_OFFERS)


def is_catalog_offer(offer_id: str) -> bool:
    """True when ``offer_id`` is a recognized operational offer id."""
    return offer_id in CATALOG_OFFER_IDS


def offer_label(offer_id: str, lang: str = "ar") -> str:
    """Bilingual label for an offer id (empty string if unknown)."""
    pair = CATALOG_OFFERS.get(offer_id)
    if pair is None:
        return ""
    return pair[0] if lang == "ar" else pair[1]


__all__ = [
    "CATALOG_OFFERS",
    "CATALOG_OFFER_IDS",
    "is_catalog_offer",
    "offer_label",
]

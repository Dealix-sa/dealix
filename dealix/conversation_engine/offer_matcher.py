"""Offer matching — pick the best-fit offer(s) for a scored target."""

from __future__ import annotations

from typing import Any

from dealix.conversation_engine import company_brain


def match_offer(target: dict[str, Any]) -> dict[str, Any]:
    """Return the best-matching offer plus ranked alternatives."""
    signals = set(target.get("signals", []))
    persona = company_brain.persona_by_id(str(target.get("persona") or ""))
    preferred = set(persona.get("preferred_offers", [])) if persona else set()

    ranked: list[tuple[int, dict[str, Any]]] = []
    for offer in company_brain.offers():
        fit_signals = set(offer.get("fit_signals", []))
        overlap = len(fit_signals.intersection(signals))
        pref_bonus = 2 if offer.get("id") in preferred else 0
        band_bonus = 1 if target.get("band") == "hot" else 0
        total = overlap * 3 + pref_bonus + band_bonus
        if total > 0:
            ranked.append((total, offer))

    if not ranked:
        # Safe default entry point: smallest paid offer.
        default = company_brain.offer_by_id("revenue_proof_sprint")
        return {
            "primary_offer_id": default["id"] if default else "revenue_proof_sprint",
            "primary_offer": default or {},
            "alternatives": [],
            "match_score": 0,
            "rationale_ar": "لا توجد إشارة قوية بعد؛ نبدأ بأصغر عرض يثبت القيمة.",
        }

    ranked.sort(key=lambda item: item[0], reverse=True)
    primary_score, primary = ranked[0]
    alternatives = [offer.get("id") for _, offer in ranked[1:3]]

    return {
        "primary_offer_id": primary.get("id"),
        "primary_offer": primary,
        "alternatives": alternatives,
        "match_score": primary_score,
        "rationale_ar": (
            f"العرض «{primary.get('name_ar')}» يطابق إشارات العميل "
            f"({', '.join(sorted(signals.intersection(set(primary.get('fit_signals', []))))) or 'عام'})."
        ),
    }

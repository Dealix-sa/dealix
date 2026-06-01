"""Route a scored company to recommended offers from 03_OFFERS.yml."""
from __future__ import annotations

from .config_loader import load_offers


def route(scored_company: dict) -> list[dict]:
    """Return a prioritised list of offer dicts for *scored_company*.

    *scored_company* must contain at minimum a ``score`` key (float/int).
    Optional keys: ``sector``, ``budget_sar``, ``company_size``.

    Each returned dict contains: ``id``, ``name``, ``price_range_sar``,
    ``rationale``.
    """
    offers = load_offers()
    score: float = float(scored_company.get("score", 0))

    def _price_range(offer_key: str, offer_data: dict) -> str:
        if "price_sar" in offer_data:
            p = offer_data["price_sar"]
            lo = p.get("min", 0)
            hi = p.get("max", 0)
            return f"{lo:,}–{hi:,} SAR"
        if "price_sar_monthly" in offer_data:
            p = offer_data["price_sar_monthly"]
            lo = p.get("min", 0)
            hi = p.get("max", 0)
            return f"{lo:,}–{hi:,} SAR/month"
        return "contact for pricing"

    def _build(offer_key: str, rationale: str) -> dict | None:
        if offer_key not in offers:
            return None
        o = offers[offer_key]
        return {
            "id": o.get("id", offer_key),
            "name": o.get("name", offer_key),
            "price_range_sar": _price_range(offer_key, o),
            "rationale": rationale,
        }

    result: list[dict] = []

    if score >= 70:
        pilot = _build(
            "agentic_workflow_pilot",
            "High score indicates strong fit for a direct agentic pilot engagement.",
        )
        audit = _build(
            "ai_workflow_audit",
            "Entry-point audit to document current workflows before the pilot.",
        )
        if pilot:
            result.append(pilot)
        if audit:
            result.append(audit)
    elif score >= 40:
        audit = _build(
            "ai_workflow_audit",
            "Mid-range score: an audit will surface the highest-value automation opportunities.",
        )
        if audit:
            result.append(audit)
    else:
        audit = _build(
            "ai_workflow_audit",
            "Low score: a lightweight audit is the appropriate low-risk entry point.",
        )
        if audit:
            result.append(audit)

    return result

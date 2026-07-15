"""Target profiling and opportunity scoring.

Scores each target from its signals + persona pain overlap. Deterministic and
stdlib-only so scores are stable across CI runs.
"""

from __future__ import annotations

from typing import Any

from dealix.conversation_engine import company_brain

# Signal → weight. Higher weight = stronger buying signal for Dealix.
SIGNAL_WEIGHTS: dict[str, int] = {
    "lost_followup": 20,
    "leaking_leads": 20,
    "weak_followup": 18,
    "unqualified_leads": 15,
    "no_pipeline_clarity": 15,
    "has_sales_team": 12,
    "market_entry": 14,
    "needs_partners": 12,
    "wants_segments": 10,
    "enterprise_readiness": 14,
    "tenders": 10,
    "partnerships": 10,
    "needs_daily_ops": 16,
    "ongoing_followup": 14,
    "wants_command_room": 16,
}

MAX_SCORE = 100


def score_target(target: dict[str, Any]) -> dict[str, Any]:
    """Return an opportunity score (0-100) plus the reasoning breakdown."""
    signals = list(target.get("signals", []))
    persona = company_brain.persona_by_id(str(target.get("persona") or ""))

    raw = sum(SIGNAL_WEIGHTS.get(sig, 5) for sig in signals)

    # Persona pain overlap bonus: signals that match the persona's known pains.
    overlap = 0
    persona_pains = set(persona.get("pains", [])) if persona else set()
    if persona_pains:
        overlap = len(persona_pains.intersection(signals)) * 5

    score = min(MAX_SCORE, raw + overlap)

    if score >= 70:
        band = "hot"
    elif score >= 45:
        band = "warm"
    else:
        band = "cold"

    reasons = [f"signal:{sig}(+{SIGNAL_WEIGHTS.get(sig, 5)})" for sig in signals]
    if overlap:
        reasons.append(f"persona_overlap(+{overlap})")

    return {
        "company": target.get("company", ""),
        "contact_name": target.get("contact_name", ""),
        "segment": target.get("segment", ""),
        "persona": target.get("persona", ""),
        "signals": signals,
        "pain_hypothesis_ar": target.get("pain_hypothesis_ar", ""),
        "source": target.get("source", "hypothesis"),
        "score": score,
        "band": band,
        "reasons": reasons,
    }


def score_targets(targets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    scored = [score_target(t) for t in targets]
    scored.sort(key=lambda t: t["score"], reverse=True)
    return scored

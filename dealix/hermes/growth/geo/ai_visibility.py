"""
AI visibility score — composes the various GEO signals into one number.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AIVisibilityScore:
    score: float
    band: str
    drivers: dict[str, float]
    notes: list[str]


def score_ai_visibility(
    *,
    answer_pages_score: float,
    faq_coverage_score: float,
    comparison_pages_score: float,
    entity_consistency_score: float,
    trust_signal_score: float,
    review_visibility_score: float,
) -> AIVisibilityScore:
    drivers = {
        "answer_pages": answer_pages_score * 0.20,
        "faq_coverage": faq_coverage_score * 0.15,
        "comparison_pages": comparison_pages_score * 0.10,
        "entity_consistency": entity_consistency_score * 0.20,
        "trust_signals": trust_signal_score * 0.20,
        "review_visibility": review_visibility_score * 0.15,
    }
    raw = sum(drivers.values())
    score = max(0.0, min(100.0, round(raw, 2)))
    band = (
        "absent"
        if score < 25
        else "emerging"
        if score < 50
        else "competitive"
        if score < 75
        else "leading"
    )
    notes: list[str] = []
    if drivers["entity_consistency"] < 10:
        notes.append("entity inconsistency is the largest blocker")
    if drivers["trust_signals"] < 10:
        notes.append("low trust-signal coverage suppresses citation rate")
    return AIVisibilityScore(score=score, band=band, drivers=drivers, notes=notes)

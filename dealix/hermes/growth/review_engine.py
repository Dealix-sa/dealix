"""
Review engine — track review surface area for AI-search visibility.

External research suggests brands with 80+ reviews dominate AI-generated
answer surfaces. This module scores how close the brand is to that bar.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ReviewProfile:
    platform: str
    review_count: int
    average_rating: float | None
    last_review_iso: str | None


@dataclass
class ReviewVisibilityScore:
    score: float
    coverage_band: str
    profiles: list[ReviewProfile]
    notes: list[str]


_TARGET_REVIEWS_PER_PLATFORM = 80
_MIN_PLATFORMS = 2


def review_visibility(profiles: list[ReviewProfile]) -> ReviewVisibilityScore:
    if not profiles:
        return ReviewVisibilityScore(
            score=0.0,
            coverage_band="absent",
            profiles=[],
            notes=["no review platforms configured"],
        )
    total = sum(min(p.review_count, _TARGET_REVIEWS_PER_PLATFORM) for p in profiles)
    cap = _TARGET_REVIEWS_PER_PLATFORM * max(len(profiles), _MIN_PLATFORMS)
    score = round((total / cap) * 100, 2)
    notes: list[str] = []
    if len(profiles) < _MIN_PLATFORMS:
        notes.append(f"only {len(profiles)} platform(s); need >= {_MIN_PLATFORMS}")
    weak = [p.platform for p in profiles if p.review_count < 20]
    if weak:
        notes.append(f"platforms with < 20 reviews: {weak}")
    band = (
        "absent"
        if score < 10
        else "thin"
        if score < 30
        else "growing"
        if score < 60
        else "strong"
        if score < 85
        else "dominant"
    )
    return ReviewVisibilityScore(
        score=score, coverage_band=band, profiles=profiles, notes=notes
    )

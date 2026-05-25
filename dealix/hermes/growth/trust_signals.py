"""
Trust signals — case studies, reviews, evidence packs, methodology, etc.

Rule: every important marketing page must carry at least 3 distinct trust
signals from different categories.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class TrustSignalCategory(StrEnum):
    CASE_STUDY = "case_study"
    VERIFIED_OUTCOME = "verified_outcome"
    CUSTOMER_REVIEW = "customer_review"
    PARTNER_TESTIMONIAL = "partner_testimonial"
    EVIDENCE_PACK = "evidence_pack"
    PUBLIC_METHODOLOGY = "public_methodology"
    SECURITY_POSTURE = "security_posture"
    COMPANY_PROFILE = "company_profile"
    ENTITY_DATA = "entity_data"


@dataclass(frozen=True)
class TrustSignal:
    category: TrustSignalCategory
    title: str
    url: str = ""
    last_verified_iso: str = ""


@dataclass
class TrustSignalReport:
    page_id: str
    signals: list[TrustSignal]
    distinct_categories: int
    score: float
    notes: list[str]


_MIN_DISTINCT_CATEGORIES = 3
_TARGET_DISTINCT_CATEGORIES = 5


def score_trust_signals(page_id: str, signals: list[TrustSignal]) -> TrustSignalReport:
    distinct = {s.category for s in signals}
    n = len(distinct)
    raw = (n / _TARGET_DISTINCT_CATEGORIES) * 100
    score = max(0.0, min(100.0, round(raw, 2)))
    notes: list[str] = []
    if n < _MIN_DISTINCT_CATEGORIES:
        notes.append(
            f"only {n} distinct trust-signal categories; need >= {_MIN_DISTINCT_CATEGORIES}"
        )
    missing = {
        TrustSignalCategory.CASE_STUDY,
        TrustSignalCategory.VERIFIED_OUTCOME,
        TrustSignalCategory.PUBLIC_METHODOLOGY,
    } - distinct
    if missing:
        notes.append(f"missing high-impact categories: {sorted(c.value for c in missing)}")
    return TrustSignalReport(
        page_id=page_id,
        signals=signals,
        distinct_categories=n,
        score=score,
        notes=notes,
    )

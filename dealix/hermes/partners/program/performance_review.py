from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PartnerPerformanceReview:
    partner_id: str
    quarter: str
    score: float
    actions: list[str]


def review_partner_performance(
    *,
    partner_id: str,
    quarter: str,
    verified_revenue_sar: float,
    customer_satisfaction_avg: float,
    customer_complaints: int,
    enablement_score: float,
) -> PartnerPerformanceReview:
    actions: list[str] = []
    score = 0.0
    score += min(50.0, verified_revenue_sar / 5000)  # 50 pts at 250K SAR
    score += max(0.0, min(20.0, (customer_satisfaction_avg - 3.0) * 10))
    score -= customer_complaints * 5
    score += enablement_score * 0.2
    score = max(0.0, min(100.0, round(score, 2)))

    if customer_complaints >= 3:
        actions.append("trigger compliance review and freeze co-marketing")
    if enablement_score < 60:
        actions.append("re-enroll partner in enablement modules")
    if verified_revenue_sar < 25_000:
        actions.append("schedule activation call to identify blockers")
    if score >= 80:
        actions.append("nominate for tier promotion review")

    return PartnerPerformanceReview(
        partner_id=partner_id,
        quarter=quarter,
        score=score,
        actions=actions,
    )

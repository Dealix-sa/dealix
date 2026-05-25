"""
Revenue Quality — يميّز جودة الـ verified revenue:

    - recurring vs one-off
    - retained vs churned
    - partner-influenced vs direct
    - high-margin vs low-margin
"""

from __future__ import annotations

from dataclasses import dataclass

from .revenue_events import RevenueEvent, RevenueEventKind


@dataclass
class QualityScore:
    score: int  # 0..100
    reasons: list[str]
    recurring: bool
    partner_influenced: bool


class RevenueQualityScorer:
    def score(
        self,
        event: RevenueEvent,
        *,
        margin_pct: float | None = None,
        previously_retained: bool = False,
    ) -> QualityScore:
        score = 50
        reasons: list[str] = ["base score 50"]
        recurring = event.kind in {
            RevenueEventKind.RETAINER_STARTED,
            RevenueEventKind.RETAINER_RENEWED,
        }
        partner_influenced = event.partner_id is not None

        if recurring:
            score += 25
            reasons.append("recurring (+25)")
        if event.kind == RevenueEventKind.RETAINER_RENEWED and previously_retained:
            score += 10
            reasons.append("renewal after retention (+10)")
        if partner_influenced:
            score += 5
            reasons.append("partner-influenced (+5)")
        if margin_pct is not None:
            if margin_pct >= 0.6:
                score += 15
                reasons.append("margin >= 60% (+15)")
            elif margin_pct < 0.2:
                score -= 15
                reasons.append("margin < 20% (-15)")
        if event.amount_sar < 1000:
            score -= 10
            reasons.append("amount < 1000 SAR (-10)")

        score = max(0, min(100, score))
        return QualityScore(
            score=score,
            reasons=reasons,
            recurring=recurring,
            partner_influenced=partner_influenced,
        )


__all__ = ["QualityScore", "RevenueQualityScorer"]

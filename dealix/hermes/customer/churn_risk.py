"""Churn-risk evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ChurnRisk(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


@dataclass(frozen=True)
class ChurnRiskAssessment:
    customer_id: str
    risk: ChurnRisk
    reasons: tuple[str, ...]


def evaluate_churn_risk(
    *,
    customer_id: str,
    health_score: float,
    days_since_last_activity: int,
    open_tickets_critical: int,
    payment_late_days: int,
) -> ChurnRiskAssessment:
    reasons: list[str] = []
    if health_score < 0.3:
        reasons.append("low_health_score")
    if days_since_last_activity > 30:
        reasons.append("inactive_30d")
    if open_tickets_critical > 0:
        reasons.append("critical_tickets")
    if payment_late_days > 14:
        reasons.append("payment_overdue")
    if any(r in reasons for r in ("low_health_score", "payment_overdue")) or len(reasons) >= 2:
        risk = ChurnRisk.high
    elif reasons:
        risk = ChurnRisk.medium
    else:
        risk = ChurnRisk.low
    return ChurnRiskAssessment(customer_id=customer_id, risk=risk, reasons=tuple(reasons))

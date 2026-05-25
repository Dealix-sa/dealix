"""Customer health score."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HealthScore:
    customer_id: str
    score: float
    components: dict[str, float]


def compute_health_score(
    *,
    customer_id: str,
    usage_score: float,
    nps_score: float,
    paid_on_time: bool,
    open_tickets: int,
) -> HealthScore:
    usage = max(0.0, min(usage_score, 1.0)) * 0.4
    nps = max(0.0, min((nps_score + 100) / 200, 1.0)) * 0.3
    payment = 0.2 if paid_on_time else 0.0
    tickets = max(0.0, 0.1 - 0.02 * open_tickets)
    score = round(usage + nps + payment + tickets, 4)
    return HealthScore(
        customer_id=customer_id,
        score=score,
        components={"usage": usage, "nps": nps, "payment": payment, "tickets": tickets},
    )

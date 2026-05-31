"""Offer-level scale-or-kill — runs against revenue + adoption."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class OfferVerdict(StrEnum):
    scale = "scale"
    keep = "keep"
    kill = "kill"


@dataclass(frozen=True)
class OfferThresholds:
    scale_revenue_sar: float = 100_000.0
    scale_paid_customers: int = 5
    kill_revenue_floor_sar: float = 5_000.0
    kill_age_days: int = 60


def evaluate_offer(
    *,
    revenue_sar: float,
    paid_customers: int,
    age_days: int,
    thresholds: OfferThresholds | None = None,
) -> OfferVerdict:
    t = thresholds or OfferThresholds()
    if revenue_sar >= t.scale_revenue_sar and paid_customers >= t.scale_paid_customers:
        return OfferVerdict.scale
    if age_days >= t.kill_age_days and revenue_sar < t.kill_revenue_floor_sar:
        return OfferVerdict.kill
    return OfferVerdict.keep

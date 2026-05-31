"""Margin, delivery effort, retainer-potential checks."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from dealix.growth_os.revenue_proof.revenue_record import RevenueRecord


class MarginCheck(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_healthy: bool
    margin_pct: float
    threshold: float = 0.35


class DeliveryEffortCheck(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_efficient: bool
    usd_per_hour: float = Field(ge=0.0)
    threshold_usd_per_hour: float = 100.0


class RetainerPotentialCheck(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_candidate: bool
    signal_strength: float = Field(ge=0.0, le=1.0)


class ChecksBundle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    margin: MarginCheck
    delivery: DeliveryEffortCheck
    retainer: RetainerPotentialCheck


def _margin_check(record: RevenueRecord, threshold: float = 0.35) -> MarginCheck:
    return MarginCheck(
        is_healthy=record.margin_pct >= threshold,
        margin_pct=record.margin_pct,
        threshold=threshold,
    )


def _delivery_check(record: RevenueRecord, threshold: float = 100.0) -> DeliveryEffortCheck:
    hours = record.delivery_effort_hours or 0.0
    # No recorded effort -> treat as efficient by assigning full amount as rate.
    rate = record.amount_usd if hours <= 0 else record.amount_usd / hours
    return DeliveryEffortCheck(
        is_efficient=rate >= threshold,
        usd_per_hour=round(rate, 4),
        threshold_usd_per_hour=threshold,
    )


def _retainer_check(record: RevenueRecord) -> RetainerPotentialCheck:
    strength = 0.0
    if record.retainer_signal:
        strength += 0.6
    if record.status == "retainer_active":
        strength = 1.0
    elif record.attributed_partners:
        strength += 0.1
    if record.margin_pct >= 0.5:
        strength += 0.1
    strength = min(strength, 1.0)
    return RetainerPotentialCheck(
        is_candidate=strength >= 0.5,
        signal_strength=round(strength, 4),
    )


def run_all_checks(record: RevenueRecord) -> ChecksBundle:
    return ChecksBundle(
        margin=_margin_check(record),
        delivery=_delivery_check(record),
        retainer=_retainer_check(record),
    )


__all__ = [
    "ChecksBundle",
    "DeliveryEffortCheck",
    "MarginCheck",
    "RetainerPotentialCheck",
    "run_all_checks",
]

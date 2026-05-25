"""Growth dashboard snapshot — section 42 of the spec."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


def _utcnow() -> datetime:
    return datetime.now(UTC)


class GrowthDashboardSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid")

    period_start: datetime
    period_end: datetime
    # Top of funnel
    visitors: int = Field(default=0, ge=0)
    qualified_leads: int = Field(default=0, ge=0)
    discovery_calls: int = Field(default=0, ge=0)
    # Conversion
    proposals_sent: int = Field(default=0, ge=0)
    proposals_won: int = Field(default=0, ge=0)
    proposals_lost: int = Field(default=0, ge=0)
    # Money
    pipeline_value_usd: float = Field(default=0.0, ge=0.0)
    real_revenue_usd: float = Field(default=0.0, ge=0.0)
    retainer_revenue_usd: float = Field(default=0.0, ge=0.0)
    # Health
    avg_margin_pct: float = Field(default=0.0)
    avg_delivery_hours: float = Field(default=0.0, ge=0.0)
    # Attribution
    revenue_by_channel: dict[str, float] = Field(default_factory=dict)
    revenue_by_offer: dict[str, float] = Field(default_factory=dict)
    revenue_by_partner: dict[str, float] = Field(default_factory=dict)
    # Experiments
    experiments_running: int = Field(default=0, ge=0)
    experiments_decided: int = Field(default=0, ge=0)
    # Marketing hygiene
    vanity_metric_attempts_blocked: int = Field(default=0, ge=0)
    operating_rule_violations: int = Field(default=0, ge=0)

    generated_at: datetime = Field(default_factory=_utcnow)

    def win_rate(self) -> float:
        total = self.proposals_won + self.proposals_lost
        return 0.0 if total == 0 else round(self.proposals_won / total, 4)

    def retainer_share(self) -> float:
        if self.real_revenue_usd <= 0:
            return 0.0
        return round(self.retainer_revenue_usd / self.real_revenue_usd, 4)


def build_snapshot(payload: dict[str, Any]) -> GrowthDashboardSnapshot:
    """Build a snapshot from a flat dict; missing fields default to 0/empty."""
    return GrowthDashboardSnapshot.model_validate(payload)


__all__ = ["GrowthDashboardSnapshot", "build_snapshot"]

"""RevenueRecord pydantic model — the canonical Revenue Object."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from dealix.growth_os.revenue_proof.statuses import RevenueStatus


def _utcnow() -> datetime:
    return datetime.now(UTC)


VerificationType = Literal[
    "payment",
    "signed_agreement",
    "invoice",
    "retainer_active",
    "partner_paid",
]


class VerificationDoc(BaseModel):
    """A pointer to the verifying artifact (no PII, no raw doc body)."""

    model_config = ConfigDict(extra="forbid")

    kind: VerificationType
    reference: str = Field(..., min_length=1)
    occurred_at: datetime = Field(default_factory=_utcnow)
    amount_usd: float | None = None


class RevenueRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    record_id: str = Field(..., min_length=1)
    customer_id: str = Field(..., min_length=1)
    offer_key: str = Field(..., min_length=1)
    amount_usd: float = Field(..., ge=0.0)
    status: RevenueStatus
    verification: VerificationDoc | None = None
    attributed_channels: list[str] = Field(default_factory=list)
    attributed_assets: list[str] = Field(default_factory=list)
    attributed_agents: list[str] = Field(default_factory=list)
    attributed_partners: list[str] = Field(default_factory=list)
    attributed_campaigns: list[str] = Field(default_factory=list)
    delivery_effort_hours: float = Field(default=0.0, ge=0.0)
    margin_pct: float = Field(default=0.0, ge=-1.0, le=1.0)
    retainer_signal: bool = False
    created_at: datetime = Field(default_factory=_utcnow)


__all__ = ["RevenueRecord", "VerificationDoc", "VerificationType"]

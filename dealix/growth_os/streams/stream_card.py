"""RevenueStreamCard — a card describing a single revenue stream."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Repeatability = Literal["one_off", "occasional", "recurring", "retainer_native"]
Risk = Literal["low", "medium", "high"]


class RevenueStreamCard(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stream_key: str = Field(..., min_length=1)
    bucket: str = Field(..., min_length=1)
    label_ar: str
    label_en: str
    current_revenue_usd: float = Field(default=0.0, ge=0.0)
    pipeline_usd: float = Field(default=0.0, ge=0.0)
    margin_pct: float = Field(default=0.0)
    effort_hours_per_unit: float = Field(default=0.0, ge=0.0)
    repeatability: Repeatability = "occasional"
    retainer_potential: float = Field(default=0.0, ge=0.0, le=1.0)
    risk: Risk = "medium"
    decision: str = "pending"


__all__ = ["Repeatability", "RevenueStreamCard", "Risk"]

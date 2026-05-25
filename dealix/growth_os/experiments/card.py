"""ExperimentCard — the hypothesis + variant container for marketing tests."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


def _utcnow() -> datetime:
    return datetime.now(UTC)


class ExperimentCard(BaseModel):
    model_config = ConfigDict(extra="forbid")

    experiment_id: str = Field(..., min_length=1)
    hypothesis: str = Field(..., min_length=8)
    audience: str = Field(..., min_length=1)
    variant_a: str = Field(..., min_length=1)
    variant_b: str = Field(..., min_length=1)
    success_metric: str = Field(..., min_length=1)
    minimum_sample: int = Field(..., gt=0)
    decision_rule: str = Field(
        default="winner_must_be_2x_with_min_sample",
        min_length=1,
    )
    created_at: datetime = Field(default_factory=_utcnow)


class ExperimentResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    variant_a_outcome: float = Field(ge=0.0)
    variant_b_outcome: float = Field(ge=0.0)
    variant_a_sample: int = Field(ge=0)
    variant_b_sample: int = Field(ge=0)


__all__ = ["ExperimentCard", "ExperimentResult"]

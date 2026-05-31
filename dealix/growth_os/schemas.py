"""Shared pydantic schemas for Growth OS.

All models use ``ConfigDict(extra="forbid")`` to lock the surface area.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


def _utcnow() -> datetime:
    return datetime.now(UTC)


class BilingualLabel(BaseModel):
    """A pair of Arabic + English strings used across the Growth OS surface."""

    model_config = ConfigDict(extra="forbid")

    ar: str = Field(..., min_length=1)
    en: str = Field(..., min_length=1)


class GovernedResponse(BaseModel):
    """Standard envelope returned by Growth OS endpoints."""

    model_config = ConfigDict(extra="forbid")

    payload: dict[str, Any]
    governance_decision: str = "ALLOW"
    generated_at: datetime = Field(default_factory=_utcnow)


__all__ = ["BilingualLabel", "GovernedResponse"]

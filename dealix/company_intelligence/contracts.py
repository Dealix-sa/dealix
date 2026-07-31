"""Stable contracts for the canonical Company Brain facade.

These models are intentionally persistence-neutral and network-free. They
provide one normalized view while existing builders remain authoritative for
legacy compatibility until callers are migrated deliberately.
"""
from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class CompanyBrainSource(StrEnum):
    """Supported sources feeding the canonical facade."""

    INTERNAL_SNAPSHOT = "internal_snapshot"
    CUSTOMER_V6 = "customer_v6"


class ProvenanceRef(BaseModel):
    """Evidence pointer used to explain where a normalized fact came from."""

    model_config = ConfigDict(extra="forbid")

    source_type: CompanyBrainSource
    source_id: str = Field(..., min_length=1)
    tenant_id: str = Field(..., min_length=1)
    observed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class CanonicalCompanyBrain(BaseModel):
    """Normalized read-only Company Brain contract.

    The facade does not replace the current builders. It preserves their
    behavior and makes their outputs consumable through one stable shape.
    """

    model_config = ConfigDict(extra="forbid")

    schema_version: int = 1
    tenant_id: str = Field(..., min_length=1)
    company_handle: str = Field(..., min_length=1)
    source: CompanyBrainSource
    generated_at: datetime
    mission: str = ""
    sector: str = ""
    region: str = ""
    offer: str = ""
    ideal_customer_profile: str = ""
    tone_preference: str = "professional"
    language_preference: str = "ar"
    current_priorities: list[str] = Field(default_factory=list)
    pain_points: list[str] = Field(default_factory=list)
    allowed_channels: list[str] = Field(default_factory=list)
    blocked_channels: list[str] = Field(default_factory=list)
    next_best_action: str = ""
    health_overall: str = "unknown"
    guardrails: dict[str, bool] = Field(default_factory=dict)
    risk_profile: dict[str, object] = Field(default_factory=dict)
    provenance: list[ProvenanceRef] = Field(default_factory=list)

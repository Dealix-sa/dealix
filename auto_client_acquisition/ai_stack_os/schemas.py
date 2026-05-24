"""Pydantic schemas for the AI Stack — input, per-layer result, full run result.

Pydantic is the canonical validation surface across the Dealix API; the
orchestrator publishes its inputs and outputs through these models so the
HTTP layer (``api/routers/ai_stack.py``) can serialize them without a
manual mapping step.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

# Canonical offer tier identifiers (mirror ``proof_os.VALID_OFFER_TIERS``).
_VALID_OFFER_TIERS: frozenset[str] = frozenset(
    {
        "free_diagnostic",
        "sprint_499",
        "data_pack_1500",
        "managed_ops",
        "custom_ai",
    }
)


class Offer(StrEnum):
    FREE_DIAGNOSTIC = "free_diagnostic"
    SPRINT_499 = "sprint_499"
    DATA_PACK_1500 = "data_pack_1500"
    MANAGED_OPS = "managed_ops"
    CUSTOM_AI = "custom_ai"


class LayerStatus(StrEnum):
    OK = "ok"
    SKIPPED = "skipped"
    DEGRADED = "degraded"
    BLOCKED = "blocked"
    ERROR = "error"


class SourcePassportInput(BaseModel):
    """Minimal Source Passport descriptor the AI Stack needs to gate L1."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    source_id: str = Field(min_length=1)
    source_type: str = Field(default="customer_intake")
    owner: str = Field(min_length=1)
    allowed_use: list[str] = Field(default_factory=list)
    contains_pii: bool = False
    sensitivity: str = Field(default="internal")
    retention_policy: str = Field(default="365d")
    ai_access_allowed: bool = True
    external_use_allowed: bool = False

    @field_validator("allowed_use")
    @classmethod
    def _normalize_uses(cls, value: list[str]) -> list[str]:
        if not value:
            return ["ai_assist"]
        return [v.strip().lower() for v in value if v and v.strip()]


class AIStackInput(BaseModel):
    """Single input record for an AI Stack run.

    Fields mirror the five productized offers' diagnostic intake: company
    name + sector + challenge + optional context document(s) the customer
    or founder is willing to share for grounding.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    tenant_id: str = Field(min_length=1)
    customer_handle: str = Field(min_length=1)
    company_name: str = Field(min_length=1, max_length=200)
    sector: str = Field(default="general", max_length=80)
    challenge_ar: str = Field(min_length=3, max_length=2000)
    challenge_en: str = Field(default="", max_length=2000)
    offer_tier: Offer = Field(default=Offer.FREE_DIAGNOSTIC)
    source_passport: SourcePassportInput
    rag_documents: list[dict[str, Any]] = Field(default_factory=list)
    actor: str = Field(default="system", max_length=120)
    locale_primary: str = Field(default="ar", pattern=r"^(ar|en)$")

    @field_validator("offer_tier", mode="before")
    @classmethod
    def _coerce_offer_tier(cls, value: Any) -> Any:
        if isinstance(value, str) and value in _VALID_OFFER_TIERS:
            return value
        if isinstance(value, Offer):
            return value
        if isinstance(value, str):
            raise ValueError(
                f"unknown offer_tier: {value!r} (allowed: {sorted(_VALID_OFFER_TIERS)})"
            )
        return value


class LayerResult(BaseModel):
    """Outcome of a single layer in the stack."""

    model_config = ConfigDict(extra="forbid")

    layer: str
    status: LayerStatus
    summary_ar: str
    summary_en: str
    duration_ms: int = 0
    payload: dict[str, Any] = Field(default_factory=dict)
    blocked_reason: str | None = None


class AIStackResult(BaseModel):
    """Full result of an AI Stack run."""

    model_config = ConfigDict(extra="forbid")

    run_id: str
    tenant_id: str
    customer_handle: str
    offer_tier: Offer
    started_at: datetime
    completed_at: datetime
    duration_ms: int
    layers: list[LayerResult]
    proof_pack_id: str | None = None
    proof_score: int = 0
    decision_passport_ids: list[str] = Field(default_factory=list)
    evidence_head_hash: str = ""
    governance_blocked: bool = False
    doctrine_clean: bool = True
    recommended_offer: str = ""
    proof_pack_markdown: str = ""


__all__ = [
    "AIStackInput",
    "AIStackResult",
    "LayerResult",
    "LayerStatus",
    "Offer",
    "SourcePassportInput",
]

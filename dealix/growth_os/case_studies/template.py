"""CaseStudy schema — Before / Action / Output / Outcome / Learning / Next."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Final

from pydantic import BaseModel, ConfigDict, Field


def _utcnow() -> datetime:
    return datetime.now(UTC)


CASE_STUDY_SECTIONS: Final[tuple[str, ...]] = (
    "before",
    "action",
    "output",
    "outcome",
    "learning",
    "next",
)


class CaseStudy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str = Field(..., min_length=1)
    customer_label: str = Field(..., min_length=1, description="Generic label, no PII")
    icp_key: str
    offer_key: str
    before: str = Field(..., min_length=20)
    action: str = Field(..., min_length=20)
    output: str = Field(..., min_length=20)
    outcome: str = Field(..., min_length=20)
    learning: str = Field(..., min_length=20)
    next_step: str = Field(..., min_length=10)
    revenue_record_id: str = ""
    proof_pack_id: str = ""
    created_at: datetime = Field(default_factory=_utcnow)


def validate_case_study(case: CaseStudy) -> list[str]:
    """Return missing-section keys (always empty if pydantic accepted)."""
    missing: list[str] = []
    for s in CASE_STUDY_SECTIONS:
        value = getattr(case, "next_step" if s == "next" else s)
        if not value or not value.strip():
            missing.append(s)
    return missing


__all__ = ["CASE_STUDY_SECTIONS", "CaseStudy", "validate_case_study"]

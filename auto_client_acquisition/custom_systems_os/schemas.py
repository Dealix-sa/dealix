"""Custom Systems OS — shared dataclasses (pure core, no FastAPI/Pydantic).

Mirrors the repo convention: frozen, slots dataclasses for the pure-function
core; the FastAPI router owns its own Pydantic request/response models.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class CustomSystemEntryDecision:
    """Verdict of the governed entry gate (the coded ``>=3 paid pilots`` rule)."""

    allowed: bool
    blocked_reasons: tuple[str, ...]
    delivery_mode: str
    disclosure_ar: str
    disclosure_en: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CustomDesignProfile:
    """Per-client design tokens that OVERRIDE Dealix defaults."""

    customer_id: str
    base_source_path: str
    direction_name: str
    tokens: dict[str, Any]
    overrides_applied: tuple[str, ...]
    forbidden_copy: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CustomStructureBlueprint:
    """Per-client internal-system architecture (deterministic, ask-first)."""

    customer_id: str
    modules: tuple[dict[str, Any], ...]
    data_model: tuple[dict[str, Any], ...]
    workflows: tuple[dict[str, Any], ...]
    governance_gates: tuple[str, ...]
    missing_context_questions: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CustomSystemEngagementResult:
    """Outcome of one governed custom-system engagement."""

    engagement_id: str
    customer_id: str
    entry: CustomSystemEntryDecision
    passport_valid: bool
    passport_reasons: tuple[str, ...]
    governance_decision: str
    governance_blocked: bool
    safety_passed: bool
    safety_blocked_reasons: tuple[str, ...]
    spec_written_files: tuple[str, ...]
    proof_score: int
    proof_band: str
    proof_complete: bool
    capital_assets: tuple[str, ...]
    retainer: dict[str, Any]
    blocked_reasons: tuple[str, ...]
    delivery_mode: str
    next_step: str

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["entry"] = self.entry.to_dict()
        return data


@dataclass(frozen=True, slots=True)
class CustomSystemRecord:
    """JSONL ledger row for a custom-system engagement (tenant-scoped)."""

    engagement_id: str
    customer_id: str
    entry_allowed: bool
    passport_valid: bool
    governance_decision: str
    governance_blocked: bool
    safety_passed: bool
    proof_score: int
    proof_band: str
    proof_complete: bool
    capital_asset_ids: tuple[str, ...] = ()
    spec_written_files: tuple[str, ...] = ()
    retainer_offer: str = ""
    next_step: str = ""
    delivery_mode: str = "founder_assisted"
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


__all__ = [
    "CustomDesignProfile",
    "CustomStructureBlueprint",
    "CustomSystemEngagementResult",
    "CustomSystemEntryDecision",
    "CustomSystemRecord",
]

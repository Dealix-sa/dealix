"""Capital asset type labels for ledger entries (Commercial Trust MVP)."""

from __future__ import annotations

from enum import StrEnum


class CapitalAssetType(StrEnum):
    SCORING_RULE = "scoring_rule"
    DRAFT_TEMPLATE = "draft_template"
    GOVERNANCE_RULE = "governance_rule"
    PROOF_EXAMPLE = "proof_example"
    SECTOR_INSIGHT = "sector_insight"
    PRODUCTIZATION_SIGNAL = "productization_signal"
    # Custom Systems OS — bespoke per-client artifacts.
    CUSTOM_DESIGN_PROFILE = "custom_design_profile"
    STRUCTURE_BLUEPRINT = "structure_blueprint"
    SYSTEM_SPEC = "system_spec"


__all__ = ["CapitalAssetType"]

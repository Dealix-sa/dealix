"""AssetStore — typed registry of reusable assets."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class AssetKind(StrEnum):
    MESSAGE_TEMPLATE = "message_template"
    PROPOSAL_TEMPLATE = "proposal_template"
    CASE_STUDY = "case_study"
    CHECKLIST = "checklist"
    POLICY_TEMPLATE = "policy_template"
    WORKSHOP_DECK = "workshop_deck"
    SECTOR_REPORT = "sector_report"
    PARTNER_PACK = "partner_pack"
    WORKFLOW_TEMPLATE = "workflow_template"
    AGENT_TEMPLATE = "agent_template"


@dataclass
class Asset:
    asset_id: str
    kind: AssetKind
    title: str
    owner: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    reuse_count: int = 0
    verified_revenue_influence_sar: float = 0.0
    quality_grade: str = "U"
    tags: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)


ASSET_STORE: dict[str, Asset] = {}


def register_asset(asset: Asset) -> Asset:
    ASSET_STORE[asset.asset_id] = asset
    return asset

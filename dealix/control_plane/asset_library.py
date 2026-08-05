"""
Section 68 — Asset Library.

Every reusable artefact (template, playbook, sector kit, training deck,
case study, …) is an Asset. Assets carry a score; assets that drive
revenue are flagged `commercializable=True` and feed the Marketplace.
"""

from __future__ import annotations

import uuid
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class AssetType(StrEnum):
    MESSAGE_TEMPLATE = "message_template"
    PROPOSAL_TEMPLATE = "proposal_template"
    OBJECTION_PLAYBOOK = "objection_playbook"
    CASE_STUDY = "case_study"
    TRAINING_DECK = "training_deck"
    POLICY_TEMPLATE = "policy_template"
    SECTOR_KIT = "sector_kit"
    PARTNER_PACK = "partner_pack"
    WORKFLOW_TEMPLATE = "workflow_template"
    AGENT_TEMPLATE = "agent_template"
    MARKET_REPORT = "market_report"


@dataclass
class AssetScore:
    reuse_count: int = 0
    revenue_influenced_sar: float = 0.0
    conversion_impact: float = 0.0
    quality_score: float = 0.0
    trust_score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "reuse_count": self.reuse_count,
            "revenue_influenced_sar": self.revenue_influenced_sar,
            "conversion_impact": self.conversion_impact,
            "quality_score": self.quality_score,
            "trust_score": self.trust_score,
        }


@dataclass
class Asset:
    asset_id: str
    name: str
    type: AssetType
    workspace_id: str
    owner_identity_id: str
    tags: list[str] = field(default_factory=list)
    score: AssetScore = field(default_factory=AssetScore)
    commercializable: bool = False
    productized_as_offer_id: str | None = None
    body_ref: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    last_used_at: datetime | None = None

    def reuse(self, *, revenue_sar: float = 0.0) -> None:
        self.score.reuse_count += 1
        self.score.revenue_influenced_sar += max(0.0, revenue_sar)
        self.last_used_at = datetime.now(UTC)

    def to_dict(self) -> dict[str, Any]:
        return {
            "asset_id": self.asset_id,
            "name": self.name,
            "type": self.type.value,
            "workspace_id": self.workspace_id,
            "owner_identity_id": self.owner_identity_id,
            "tags": list(self.tags),
            "score": self.score.to_dict(),
            "commercializable": self.commercializable,
            "productized_as_offer_id": self.productized_as_offer_id,
            "body_ref": self.body_ref,
            "created_at": self.created_at.isoformat(),
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
        }


class AssetLibrary:
    def __init__(self) -> None:
        self._assets: dict[str, Asset] = {}

    def create(
        self,
        *,
        name: str,
        type: AssetType,
        workspace_id: str,
        owner_identity_id: str,
        tags: Iterable[str] = (),
        body_ref: str | None = None,
    ) -> Asset:
        asset = Asset(
            asset_id=f"asset_{uuid.uuid4().hex[:12]}",
            name=name,
            type=type,
            workspace_id=workspace_id,
            owner_identity_id=owner_identity_id,
            tags=list(tags),
            body_ref=body_ref,
        )
        self._assets[asset.asset_id] = asset
        return asset

    def get(self, asset_id: str) -> Asset:
        try:
            return self._assets[asset_id]
        except KeyError as exc:
            raise KeyError(f"unknown asset: {asset_id}") from exc

    def reuse(self, asset_id: str, *, revenue_sar: float = 0.0) -> Asset:
        asset = self.get(asset_id)
        asset.reuse(revenue_sar=revenue_sar)
        return asset

    def mark_commercializable(self, asset_id: str) -> Asset:
        asset = self.get(asset_id)
        asset.commercializable = True
        return asset

    def link_offer(self, asset_id: str, *, offer_id: str) -> Asset:
        asset = self.get(asset_id)
        asset.productized_as_offer_id = offer_id
        asset.commercializable = True
        return asset

    def by_type(self, type: AssetType) -> list[Asset]:
        return [a for a in self._assets.values() if a.type is type]

    def reusable_top(self, *, limit: int = 10) -> list[Asset]:
        return sorted(self._assets.values(), key=lambda a: a.score.reuse_count, reverse=True)[
            :limit
        ]

    def underused(self, *, max_reuse: int = 1) -> list[Asset]:
        return [a for a in self._assets.values() if a.score.reuse_count <= max_reuse]

    def all(self) -> list[Asset]:
        return list(self._assets.values())

"""Phase 6: Assets — durable IP harvested from Outcomes."""

from __future__ import annotations

from dataclasses import dataclass, field

from dealix.hermes.kernel.schemas import (
    Asset,
    AssetType,
    LifecycleEvent,
    Outcome,
)
from dealix.hermes.kernel.scoring import asset_quality_score


@dataclass
class AssetStore:
    _assets: dict[str, Asset] = field(default_factory=dict)
    _events: list[LifecycleEvent] = field(default_factory=list)

    def review_outcome(self, outcome: Outcome) -> bool:
        """Doctrine: every Outcome must be reviewed for Asset potential."""
        if outcome.asset_review_required:
            return True
        # Profitable + repeatable outcomes auto-flag for review.
        if outcome.margin_sar > 0 and outcome.revenue_verified:
            return True
        return False

    def create_from_outcome(
        self,
        outcome: Outcome,
        *,
        asset_type: AssetType,
        title: str,
        description: str = "",
        artifact_uri: str | None = None,
        moat_score: float = 0.0,
        tags: list[str] | None = None,
    ) -> Asset:
        if not self.review_outcome(outcome) and not outcome.asset_review_required:
            raise ValueError(f"outcome {outcome.outcome_id} not eligible for asset creation")
        asset = Asset(
            outcome_id=outcome.outcome_id,
            asset_type=asset_type,
            title=title,
            description=description,
            artifact_uri=artifact_uri,
            moat_score=moat_score,
            tags=tags or [],
        )
        self._assets[asset.asset_id] = asset
        self._events.append(LifecycleEvent(
            event_type="asset.created",
            entity_id=asset.asset_id,
            payload={"asset_type": asset_type.value, "title": title},
        ))
        return asset

    def record_reuse(self, asset_id: str, revenue_sar: float = 0.0) -> Asset:
        a = self._assets[asset_id]
        new_reuse = a.reuse_count + 1
        new_revenue = a.revenue_attributed_sar + revenue_sar
        score = asset_quality_score(
            reuse_count=new_reuse,
            revenue_attributed_sar=new_revenue,
            moat_score=a.moat_score,
        )
        updated = a.model_copy(update={
            "reuse_count": new_reuse,
            "revenue_attributed_sar": new_revenue,
            "quality_score": score,
        })
        self._assets[asset_id] = updated
        return updated

    def scale(self, asset_id: str) -> Asset:
        a = self._assets[asset_id]
        updated = a.model_copy(update={"scaled": True, "killed": False})
        self._assets[asset_id] = updated
        self._events.append(LifecycleEvent(event_type="asset.scaled", entity_id=asset_id))
        return updated

    def kill(self, asset_id: str, reason: str = "") -> Asset:
        a = self._assets[asset_id]
        updated = a.model_copy(update={"killed": True, "scaled": False})
        self._assets[asset_id] = updated
        self._events.append(LifecycleEvent(
            event_type="asset.killed",
            entity_id=asset_id,
            payload={"reason": reason},
        ))
        return updated

    def get(self, asset_id: str) -> Asset:
        return self._assets[asset_id]

    def list(self) -> list[Asset]:
        return list(self._assets.values())

    def events(self) -> list[LifecycleEvent]:
        return list(self._events)

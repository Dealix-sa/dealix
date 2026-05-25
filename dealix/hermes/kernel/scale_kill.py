"""Phase 7: Scale or Kill. No Asset lives forever without proof of value."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from dealix.hermes.kernel.assets import AssetStore
from dealix.hermes.kernel.schemas import Asset


class ScaleKillVerdict(StrEnum):
    scale = "scale"
    keep = "keep"
    kill = "kill"


@dataclass
class ScaleKillThresholds:
    scale_reuse: int = 5
    scale_revenue_sar: float = 50_000.0
    scale_quality: float = 0.6
    kill_age_days_no_reuse: int = 90
    kill_quality_floor: float = 0.05


def evaluate(asset: Asset, thresholds: ScaleKillThresholds | None = None) -> ScaleKillVerdict:
    t = thresholds or ScaleKillThresholds()
    if (
        asset.reuse_count >= t.scale_reuse
        and asset.revenue_attributed_sar >= t.scale_revenue_sar
        and asset.quality_score >= t.scale_quality
    ):
        return ScaleKillVerdict.scale
    if asset.quality_score < t.kill_quality_floor and asset.reuse_count == 0:
        return ScaleKillVerdict.kill
    return ScaleKillVerdict.keep


def apply_verdict(
    store: AssetStore,
    asset_id: str,
    verdict: ScaleKillVerdict | None = None,
) -> Asset:
    asset = store.get(asset_id)
    v = verdict or evaluate(asset)
    if v == ScaleKillVerdict.scale:
        return store.scale(asset_id)
    if v == ScaleKillVerdict.kill:
        return store.kill(asset_id, reason="failed_scale_kill_thresholds")
    return asset

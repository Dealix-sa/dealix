"""AssetQuality — grade assets by reuse, revenue influence, and freshness."""

from __future__ import annotations

from datetime import UTC, datetime

from dealix.hermes.assets.asset_store import Asset


def grade_asset(asset: Asset, *, now: datetime | None = None) -> str:
    now = now or datetime.now(UTC)
    age_days = max(1, (now - asset.created_at).days)
    revenue_score = min(1.0, asset.verified_revenue_influence_sar / 100_000.0)
    reuse_score = min(1.0, asset.reuse_count / 10.0)
    freshness = max(0.0, 1.0 - age_days / 365.0)
    score = 0.5 * revenue_score + 0.3 * reuse_score + 0.2 * freshness
    if score >= 0.7:
        grade = "A"
    elif score >= 0.45:
        grade = "B"
    elif score >= 0.2:
        grade = "C"
    else:
        grade = "D"
    asset.quality_grade = grade
    return grade

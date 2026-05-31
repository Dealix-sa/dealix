"""Asset scoring delegate."""

from __future__ import annotations

from dealix.hermes.kernel.scoring import asset_quality_score


def score_asset(*, reuse_count: int, revenue_attributed_sar: float, moat_score: float) -> float:
    return asset_quality_score(
        reuse_count=reuse_count,
        revenue_attributed_sar=revenue_attributed_sar,
        moat_score=moat_score,
    )

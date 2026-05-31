"""ICP scoring rewards industry, region, size, and pain overlap."""

from __future__ import annotations

from dealix.hermes.growth.icp_registry import ICP, reset, score_account, upsert


def test_icp_score_account_matches_attributes() -> None:
    reset()
    upsert(
        ICP(
            icp_id="icp_logistics_sa",
            name="Saudi logistics mid",
            industry="logistics",
            region="SA",
            company_size="medium",
            pain_points=("manual_routing", "high_idle_time"),
        )
    )
    score = score_account(
        "icp_logistics_sa",
        {"industry": "logistics", "region": "SA", "company_size": "medium", "pain_points": ["manual_routing"]},
    )
    assert score > 0.7

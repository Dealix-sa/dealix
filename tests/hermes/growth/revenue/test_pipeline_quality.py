"""Pipeline quality weighs deals by stage, ICP fit, age and proof."""

from __future__ import annotations

from dealix.hermes.growth.revenue.pipeline_quality import PipelineDeal, assess


def test_proof_backed_late_stage_deals_grade_higher() -> None:
    deals = [
        PipelineDeal("d1", icp_fit=0.9, stage="negotiation", age_days=30, has_proof_pack=True, amount_sar=200_000),
        PipelineDeal("d2", icp_fit=0.8, stage="proposal", age_days=20, has_proof_pack=True, amount_sar=120_000),
    ]
    rep = assess(deals)
    assert rep.total_value_sar == 320_000
    assert rep.grade in {"A", "B", "C"}
    assert rep.quality_ratio > 0

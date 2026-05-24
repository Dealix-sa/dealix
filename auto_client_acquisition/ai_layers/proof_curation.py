"""Layer 6 — Proof curation: pick best artifacts for a sales context.

Curates from a pool of proof artifacts (proof_pack ids, case-safe summaries,
capital assets, value_ledger entries). Never invents proofs. Only selects what
is already available. If pool is empty → BLOCK.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.ai_layers.schemas import LayerContext, LayerResult

_SECTOR_BOOST = {
    "fintech": {"governance_rule": 3, "proof_example": 2, "sector_insight": 3},
    "saas": {"draft_template": 2, "proof_example": 2, "scoring_rule": 2},
    "ecommerce": {"draft_template": 3, "scoring_rule": 2},
    "manufacturing": {"sector_insight": 3, "qa_rubric": 2},
    "default": {"proof_example": 2, "scoring_rule": 1, "draft_template": 1},
}

_STAGE_BOOST = {
    "discovery": {"sector_insight": 3, "draft_template": 1},
    "diagnosis": {"proof_example": 3, "scoring_rule": 2},
    "proposal": {"proof_example": 4, "governance_rule": 3},
    "kickoff": {"qa_rubric": 2, "draft_template": 2},
    "renewal": {"productization_signal": 3, "proof_example": 2},
}


def _score_artifact(
    artifact: dict[str, Any],
    sector: str,
    stage: str,
) -> int:
    score = 0
    a_type = str(artifact.get("type", ""))
    tier = str(artifact.get("tier", "estimated"))
    # Tier strength
    score += {
        "estimated": 1,
        "observed": 3,
        "verified": 5,
        "client_confirmed": 7,
    }.get(tier, 0)
    # Sector affinity
    sect_map = _SECTOR_BOOST.get(sector, _SECTOR_BOOST["default"])
    score += sect_map.get(a_type, 0)
    # Stage affinity
    stage_map = _STAGE_BOOST.get(stage, {})
    score += stage_map.get(a_type, 0)
    return score


def run(ctx: LayerContext) -> LayerResult:
    """Pick top-N proof artifacts for the sales context.

    Expected payload keys:
        sector: str — fintech / saas / ecommerce / manufacturing / default.
        stage: str — discovery / diagnosis / proposal / kickoff / renewal.
        artifacts: list[dict] — each {id, type, tier, source_ref, summary}.
        top_n: int — default 3.
    """
    sector = str(ctx.payload.get("sector", "default")).lower()
    stage = str(ctx.payload.get("stage", "discovery")).lower()
    artifacts = list(ctx.payload.get("artifacts", []) or [])
    top_n = int(ctx.payload.get("top_n", 3) or 3)

    if not artifacts:
        return LayerResult(
            layer="proof_curation",
            customer_id=ctx.customer_id,
            ok=False,
            governance_decision="BLOCK",
            output={"reason": "no_artifacts_available", "sector": sector, "stage": stage},
            notes=("Proof curation needs at least one artifact",),
        )

    # Drop any artifact without a source_ref (no source → no answer doctrine).
    sourced = [a for a in artifacts if a.get("source_ref")]
    if not sourced:
        return LayerResult(
            layer="proof_curation",
            customer_id=ctx.customer_id,
            ok=False,
            governance_decision="BLOCK",
            output={"reason": "no_source_ref_on_any_artifact"},
            notes=("All artifacts missing source_ref",),
        )

    ranked = sorted(
        sourced,
        key=lambda a: _score_artifact(a, sector, stage),
        reverse=True,
    )
    chosen = ranked[: max(1, top_n)]

    return LayerResult(
        layer="proof_curation",
        customer_id=ctx.customer_id,
        ok=True,
        governance_decision="ALLOW",
        output={
            "sector": sector,
            "stage": stage,
            "selected": [
                {
                    "id": a.get("id"),
                    "type": a.get("type"),
                    "tier": a.get("tier"),
                    "source_ref": a.get("source_ref"),
                    "summary": a.get("summary", ""),
                    "score": _score_artifact(a, sector, stage),
                }
                for a in chosen
            ],
            "considered": len(sourced),
        },
        notes=(f"selected {len(chosen)} of {len(sourced)} sourced",),
        capital_asset_candidates=("proof_example",),
    )

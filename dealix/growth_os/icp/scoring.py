"""ICP fit scoring — pure function from account signals to a fit score."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.growth_os.icp.matrix import ICP_MATRIX, ICPDefinition


class ICPFitScore(BaseModel):
    model_config = ConfigDict(extra="forbid")

    icp_key: str
    score: float = Field(..., ge=0.0, le=1.0)
    matched_signals: list[str]
    missing_signals: list[str]
    band: str  # strong | moderate | weak | reject


def _band_for(score: float, disqualified: bool) -> str:
    if disqualified:
        return "reject"
    if score >= 0.75:
        return "strong"
    if score >= 0.5:
        return "moderate"
    return "weak"


def _signal_strength(signals: dict[str, Any], icp: ICPDefinition) -> tuple[float, list[str], list[str], bool]:
    matched: list[str] = []
    missing: list[str] = []

    pains = [p.lower() for p in signals.get("pains", [])]
    if any(p in icp.primary_pain_en.lower() or p in icp.primary_pain_ar for p in pains):
        matched.append("pain_match")
    else:
        missing.append("pain_match")

    dms = [d.lower() for d in signals.get("decision_makers", [])]
    if any(dm in icp.decision_makers for dm in dms):
        matched.append("decision_maker_match")
    else:
        missing.append("decision_maker_match")

    arr = signals.get("estimated_arr_usd", 0)
    lo, hi = icp.typical_arr_band_usd
    if lo <= arr <= hi:
        matched.append("arr_band_match")
    else:
        missing.append("arr_band_match")

    assets = signals.get("requested_assets", [])
    if any(a in icp.proof_assets for a in assets):
        matched.append("asset_request_match")
    else:
        missing.append("asset_request_match")

    flags = signals.get("flags", [])
    disqualified = any(f in icp.disqualifiers for f in flags)

    total = 4
    score = len(matched) / total
    return score, matched, missing, disqualified


def score_icp_fit(account_signals: dict[str, Any]) -> ICPFitScore:
    """Score an account against the strongest-fit ICP.

    ``account_signals`` is a dict with keys:
      - pains: list[str]
      - decision_makers: list[str]
      - estimated_arr_usd: int
      - requested_assets: list[str]
      - flags: list[str]   (signals that may disqualify)
    """
    best: ICPFitScore | None = None
    for icp in ICP_MATRIX.values():
        score, matched, missing, disqualified = _signal_strength(account_signals, icp)
        candidate = ICPFitScore(
            icp_key=icp.key,
            score=score,
            matched_signals=matched,
            missing_signals=missing,
            band=_band_for(score, disqualified),
        )
        if best is None or candidate.score > best.score:
            best = candidate
    assert best is not None  # ICP_MATRIX is non-empty
    return best


__all__ = ["ICPFitScore", "score_icp_fit"]

"""Score a company dict against 05_SCORING.yml dimensions."""
from __future__ import annotations

from .config_loader import load_scoring


def _resolve_bucket(score: float, thresholds: dict) -> tuple[str, str]:
    """Return (bucket_key, action_text) for the given score."""
    # priority_high: min_score 80
    # priority_medium: min 60, max 79
    # nurture: min 40, max 59
    # disqualified: max 39
    for bucket_key, spec in thresholds.items():
        min_s = spec.get("min_score", 0)
        max_s = spec.get("max_score", 100)
        if min_s <= score <= max_s:
            return bucket_key, spec.get("action", "")
    # fallback: disqualified
    return "disqualified", thresholds.get("disqualified", {}).get("action", "")


def score_company(data: dict) -> dict:
    """Score *data* against the YAML scoring dimensions.

    Each dimension key in *data* should be one of the level strings defined
    in 05_SCORING.yml (e.g. ``"high"``, ``"medium"``, ``"low"`` for
    *operations_complexity*). Missing keys score 0.

    Returns a dict with keys: ``score``, ``dimensions``, ``bucket``,
    ``recommendation``.
    """
    cfg = load_scoring()
    dimensions_cfg: dict = cfg.get("scoring_dimensions", {})
    thresholds: dict = cfg.get("decision_thresholds", {})

    dimension_scores: dict[str, int] = {}
    total: float = 0.0

    for dim_key, dim_spec in dimensions_cfg.items():
        levels: dict = dim_spec.get("levels", {})
        provided_level = data.get(dim_key)
        dim_score = 0
        if provided_level is not None and provided_level in levels:
            dim_score = levels[provided_level].get("score", 0)
        dimension_scores[dim_key] = dim_score
        total += dim_score

    bucket, recommendation = _resolve_bucket(total, thresholds)

    return {
        "score": total,
        "dimensions": dimension_scores,
        "bucket": bucket,
        "recommendation": recommendation,
    }

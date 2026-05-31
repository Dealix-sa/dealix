"""A/B experiments for marketing variables (§16).

One variable per experiment. Explicit decision rule. Statistical guard:
the experiment stays `running` until both arms hit minimum_sample.
"""

from __future__ import annotations

from typing import Any

from dealix.revenue_marketing.schemas import ExperimentStatus, MarketingExperimentRecord
from dealix.revenue_marketing.store import get_revenue_marketing_store, uid


def experiment_card(
    *,
    experiment_name: str,
    target_segment: str,
    offer_id: str,
    variable_tested: str,
    variant_a: str,
    variant_b: str,
    success_metric: str,
    minimum_sample: int = 50,
    decision_rule: str = "scale variant if 2x conversion vs control",
) -> MarketingExperimentRecord:
    rec = MarketingExperimentRecord(
        id=uid("exp"),
        experiment_name=experiment_name,
        target_segment=target_segment,
        offer_id=offer_id,
        variable_tested=variable_tested,
        variant_a=variant_a,
        variant_b=variant_b,
        success_metric=success_metric,
        minimum_sample=minimum_sample,
        decision_rule=decision_rule,
        status="draft",
    )
    return get_revenue_marketing_store().upsert_experiment(rec)


def record_observation(
    *,
    experiment_id: str,
    variant: str,
    converted: bool,
) -> MarketingExperimentRecord:
    store = get_revenue_marketing_store()
    for e in store.list_experiments():
        if e.id != experiment_id:
            continue
        if variant.lower() in ("a", "variant_a"):
            e.samples_a += 1
            if converted:
                e.wins_a += 1
        elif variant.lower() in ("b", "variant_b"):
            e.samples_b += 1
            if converted:
                e.wins_b += 1
        else:
            raise ValueError("variant must be 'a' or 'b'")
        if e.status == "draft":
            e.status = "running"
        return store.upsert_experiment(e)
    raise KeyError(f"experiment not found: {experiment_id}")


def decide_experiment(experiment_id: str) -> MarketingExperimentRecord:
    """Apply the 2x-conversion rule once both arms hit minimum_sample.

    Returns the experiment with a decided status: scale, kill, or inconclusive.
    """
    store = get_revenue_marketing_store()
    target: MarketingExperimentRecord | None = None
    for e in store.list_experiments():
        if e.id == experiment_id:
            target = e
            break
    if target is None:
        raise KeyError(f"experiment not found: {experiment_id}")

    enough = target.samples_a >= target.minimum_sample and target.samples_b >= target.minimum_sample
    rate_a = (target.wins_a / target.samples_a) if target.samples_a else 0.0
    rate_b = (target.wins_b / target.samples_b) if target.samples_b else 0.0

    status: ExperimentStatus
    decision: str
    if not enough:
        status = "running"
        decision = "needs_more_samples"
    elif rate_b >= 2 * rate_a and rate_b > 0:
        status = "decided_scale"
        decision = "scale_variant_b"
    elif rate_a >= 2 * rate_b and rate_a > 0:
        status = "decided_scale"
        decision = "scale_variant_a"
    elif rate_a == 0 and rate_b == 0:
        status = "decided_kill"
        decision = "kill_both_no_conversion"
    else:
        status = "inconclusive"
        decision = "no_clear_winner"

    target.status = status
    target.decision = decision
    target.result = {
        "rate_a": round(rate_a, 4),
        "rate_b": round(rate_b, 4),
        "samples_a": target.samples_a,
        "samples_b": target.samples_b,
        "wins_a": target.wins_a,
        "wins_b": target.wins_b,
        "min_sample_met": enough,
    }
    return store.upsert_experiment(target)


def experiments_summary() -> dict[str, Any]:
    rows = get_revenue_marketing_store().list_experiments()
    by_status: dict[str, int] = {}
    for r in rows:
        by_status[r.status] = by_status.get(r.status, 0) + 1
    return {
        "total": len(rows),
        "by_status": by_status,
        "decided_scale_examples": [
            r.model_dump(mode="json") for r in rows if r.status == "decided_scale"
        ][:5],
    }

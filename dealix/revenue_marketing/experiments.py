"""Experiment lifecycle — minimum sample + 2x rule."""

from __future__ import annotations

from typing import Literal

from dealix.revenue_marketing.schemas import MarketingExperiment
from dealix.revenue_marketing.store import (
    RevenueMarketingStore,
    get_revenue_marketing_store,
    uid,
)

ExperimentDecision = Literal["scale_a", "scale_b", "kill", "extend"]

# Minimum sample (per variant) before a decision can be rendered.
MIN_SAMPLE_PER_VARIANT = 30
# Lift threshold — winning variant must beat the other by >= 2x.
LIFT_MULTIPLIER = 2.0


def create_experiment(
    experiment_name: str,
    target_segment: str,
    offer_id: str,
    variable_tested: str,
    variant_a: str,
    variant_b: str,
    success_metric: str,
    *,
    store: RevenueMarketingStore | None = None,
) -> MarketingExperiment:
    if not experiment_name:
        raise ValueError("experiment_name_required")
    if not offer_id:
        raise ValueError("offer_id_required")
    if variant_a == variant_b:
        raise ValueError("variants_must_differ")
    st = store or get_revenue_marketing_store()
    exp = MarketingExperiment(
        id=uid("exp"),
        experiment_name=experiment_name,
        target_segment=target_segment,
        offer_id=offer_id,
        variable_tested=variable_tested,
        variant_a=variant_a,
        variant_b=variant_b,
        success_metric=success_metric,
        status="running",
    )
    st.upsert_experiment(exp)
    return exp


def record_result(
    experiment_id: str,
    variant: Literal["a", "b"],
    value: float,
    *,
    store: RevenueMarketingStore | None = None,
) -> MarketingExperiment:
    """Increment the variant's running total and sample count."""
    if variant not in ("a", "b"):
        raise ValueError("variant_must_be_a_or_b")
    st = store or get_revenue_marketing_store()
    exp = next((x for x in st.list_experiments(limit=10_000) if x.id == experiment_id), None)
    if exp is None:
        raise ValueError("experiment_not_found")
    if exp.status == "decided":
        raise ValueError("experiment_already_decided")

    result = dict(exp.result)
    value_key = f"{variant}_value"
    sample_key = f"{variant}_n"
    result[value_key] = float(result.get(value_key, 0.0)) + float(value)
    result[sample_key] = float(result.get(sample_key, 0.0)) + 1.0

    updated = exp.model_copy(update={"result": result})
    st.upsert_experiment(updated)
    return updated


def decide(
    experiment_id: str,
    *,
    store: RevenueMarketingStore | None = None,
) -> ExperimentDecision:
    """Render the experiment decision per the minimum-sample + 2x rule.

    - ``extend`` when either variant lacks the minimum sample.
    - ``scale_a`` / ``scale_b`` when the winner's mean is >= 2x the loser.
    - ``kill`` when both means are zero (no signal at all).
    - ``extend`` otherwise (signal exists but no 2x lift).
    """
    st = store or get_revenue_marketing_store()
    exp = next((x for x in st.list_experiments(limit=10_000) if x.id == experiment_id), None)
    if exp is None:
        raise ValueError("experiment_not_found")

    res = exp.result
    a_n = float(res.get("a_n", 0.0))
    b_n = float(res.get("b_n", 0.0))
    a_value = float(res.get("a_value", 0.0))
    b_value = float(res.get("b_value", 0.0))

    decision: ExperimentDecision
    if a_n < MIN_SAMPLE_PER_VARIANT or b_n < MIN_SAMPLE_PER_VARIANT:
        decision = "extend"
    else:
        a_mean = a_value / a_n if a_n else 0.0
        b_mean = b_value / b_n if b_n else 0.0
        if a_mean == 0.0 and b_mean == 0.0:
            decision = "kill"
        elif a_mean >= LIFT_MULTIPLIER * max(b_mean, 1e-9):
            decision = "scale_a"
        elif b_mean >= LIFT_MULTIPLIER * max(a_mean, 1e-9):
            decision = "scale_b"
        else:
            decision = "extend"

    updated = exp.model_copy(
        update={
            "decision": decision,
            "status": "decided" if decision in ("scale_a", "scale_b", "kill") else exp.status,
        },
    )
    st.upsert_experiment(updated)
    return decision

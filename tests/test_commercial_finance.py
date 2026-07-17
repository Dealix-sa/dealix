from decimal import Decimal
from pathlib import Path

import pytest
import yaml

from dealix.commercial_finance import (
    DEFAULT_POLICIES,
    REQUIRED_ECONOMIC_SOURCE_KEYS,
    CommercialFinanceDecision,
    CommercialFinanceInputs,
    FinancePricingStatus,
    OfferEconomicsClass,
    evaluate_commercial_finance,
)
from dealix.commercial_intelligence import EvidenceLevel


def _source_refs() -> dict[str, str]:
    return {key: f"evidence://finance/{key}" for key in REQUIRED_ECONOMIC_SOURCE_KEYS}


def _inputs(**overrides: object) -> CommercialFinanceInputs:
    values: dict[str, object] = {
        "opportunity_id": "opp_1",
        "offer_id": "revenue_proof_sprint",
        "offer_class": OfferEconomicsClass.PRODUCTIZED,
        "list_price_sar": Decimal("10000"),
        "proposed_price_sar": Decimal("9000"),
        "delivery_cost_sar": Decimal("3000"),
        "acquisition_cost_sar": Decimal("500"),
        "upfront_cash_exposure_sar": Decimal("500"),
        "payment_terms_days": 30,
        "capacity_required_pct": Decimal("10"),
        "source_refs": _source_refs(),
    }
    values.update(overrides)
    return CommercialFinanceInputs(**values)  # type: ignore[arg-type]


def test_pursue_case_calculates_evidence_bound_expected_value() -> None:
    result = evaluate_commercial_finance(
        _inputs(
            close_probability_low=Decimal("0.30"),
            close_probability_base=Decimal("0.50"),
            close_probability_high=Decimal("0.70"),
            close_probability_source_ref="evidence://crm/cohort-2026-h1",
            close_probability_evidence_level=EvidenceLevel.L3_FIRST_PARTY,
            close_probability_cohort_size=12,
        )
    )

    assert result.decision is CommercialFinanceDecision.PURSUE
    assert result.gross_profit_sar == Decimal("6000.00")
    assert result.gross_margin_pct == Decimal("66.67")
    assert result.contribution_profit_sar == Decimal("5500.00")
    assert result.expected_value_base_sar == Decimal("2500.00")
    assert result.expected_value_formula == (
        "P(close) * gross_profit_if_won - acquisition_cost"
    )
    assert result.expected_value_evidence_eligible is True
    assert result.approval_required is True
    assert result.external_action_allowed is False


def test_pipeline_score_is_not_used_as_close_probability() -> None:
    result = evaluate_commercial_finance(_inputs())

    assert result.decision is CommercialFinanceDecision.PURSUE
    assert result.expected_value_base_sar is None
    assert result.expected_value_formula is None
    assert "expected_value_not_calculated_without_probability_evidence" in result.warnings


def test_probability_requires_l3_source_and_minimum_cohort() -> None:
    result = evaluate_commercial_finance(
        _inputs(
            close_probability_low=Decimal("0.30"),
            close_probability_base=Decimal("0.50"),
            close_probability_high=Decimal("0.70"),
            close_probability_source_ref="evidence://public/guess",
            close_probability_evidence_level=EvidenceLevel.L2_PUBLIC_SIGNAL,
            close_probability_cohort_size=2,
        )
    )

    assert result.decision is CommercialFinanceDecision.REVIEW
    assert result.expected_value_evidence_eligible is False
    assert result.expected_value_base_sar is None
    assert "close_probability_requires_l3_first_party_evidence" in result.evidence_gaps
    assert "close_probability_cohort_below_minimum" in result.evidence_gaps


def test_customer_roi_is_separate_and_never_rescues_bad_dealix_economics() -> None:
    result = evaluate_commercial_finance(
        _inputs(
            delivery_cost_sar=Decimal("8000"),
            customer_roi_hypothesis_sar=Decimal("1000000"),
            customer_roi_source_ref="evidence://customer/baseline",
        )
    )

    assert result.decision is CommercialFinanceDecision.STOP
    assert result.customer_roi_hypothesis_sar == Decimal("1000000.00")
    assert result.customer_roi_used_in_decision is False
    assert "gross_margin_below_floor" in result.blockers


def test_missing_financial_provenance_routes_case_to_review() -> None:
    refs = _source_refs()
    refs.pop("delivery_cost_sar")
    result = evaluate_commercial_finance(_inputs(source_refs=refs))

    assert result.decision is CommercialFinanceDecision.REVIEW
    assert "missing_source_ref:delivery_cost_sar" in result.evidence_gaps


def test_discount_and_capacity_policy_fail_closed() -> None:
    result = evaluate_commercial_finance(
        _inputs(
            proposed_price_sar=Decimal("7000"),
            delivery_cost_sar=Decimal("2500"),
            capacity_required_pct=Decimal("30"),
        )
    )

    assert result.decision is CommercialFinanceDecision.STOP
    assert "discount_above_ceiling" in result.blockers
    assert "capacity_required_above_policy" in result.blockers


@pytest.mark.parametrize("value", ["NaN", "Infinity", "-Infinity"])
def test_non_finite_financial_values_are_rejected(value: str) -> None:
    with pytest.raises(ValueError, match="must be finite"):
        _inputs(proposed_price_sar=Decimal(value))


def test_source_keys_and_refs_are_bounded() -> None:
    with pytest.raises(ValueError, match="keys must be 1-64"):
        _inputs(source_refs={"k" * 65: "evidence://x"})
    with pytest.raises(ValueError, match="values must be 1-1000"):
        _inputs(source_refs={"list_price_sar": "x" * 1001})


def test_approval_status_can_only_be_applied_by_rebuilding_immutable_inputs() -> None:
    draft = _inputs()
    approved = CommercialFinanceInputs.from_dict(
        draft.to_dict(),
        pricing_status=FinancePricingStatus.FOUNDER_APPROVED,
    )
    result = evaluate_commercial_finance(approved)

    assert result.price_approved is True
    assert result.pricing_status is FinancePricingStatus.FOUNDER_APPROVED
    assert result.external_action_allowed is False


def test_runtime_finance_policy_matches_governed_pricing_configuration() -> None:
    config = yaml.safe_load(
        (Path(__file__).resolve().parents[1] / "data/commercial/pricing_rules.yaml").read_text(
            encoding="utf-8"
        )
    )["finance_decision_rules"]

    assert set(config["required_source_refs"]) == REQUIRED_ECONOMIC_SOURCE_KEYS
    assert config["expected_value_formula"] == (
        "P(close) * gross_profit_if_won - acquisition_cost"
    )
    assert config["customer_roi"]["used_in_commercial_finance_decision"] is False
    for offer_class, policy in DEFAULT_POLICIES.items():
        configured = config["offer_classes"][offer_class.value]
        assert Decimal(str(configured["gross_margin_floor"])) == policy.gross_margin_floor
        assert Decimal(str(configured["contribution_margin_floor"])) == (
            policy.contribution_margin_floor
        )

"""Evidence-bound commercial finance decisions for Dealix.

The module evaluates Dealix's own unit economics.  It deliberately keeps any
customer ROI hypothesis separate, never treats a pipeline score as a close
probability, and never authorizes publishing a price, charging a customer, or
making an external commitment.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_CEILING, ROUND_HALF_UP, Decimal, InvalidOperation
from enum import StrEnum
from typing import Any, Mapping

from dealix.commercial_intelligence import EvidenceLevel

MONEY_QUANTUM = Decimal("0.01")
RATIO_QUANTUM = Decimal("0.0001")
PERCENT_QUANTUM = Decimal("0.01")
_EVIDENCE_RANK = {
    EvidenceLevel.L0_UNKNOWN: 0,
    EvidenceLevel.L1_HYPOTHESIS: 1,
    EvidenceLevel.L2_PUBLIC_SIGNAL: 2,
    EvidenceLevel.L3_FIRST_PARTY: 3,
    EvidenceLevel.L4_VERIFIED: 4,
    EvidenceLevel.L5_MEASURED_OUTCOME: 5,
}
REQUIRED_ECONOMIC_SOURCE_KEYS = frozenset(
    {
        "offer_class",
        "list_price_sar",
        "proposed_price_sar",
        "delivery_cost_sar",
        "acquisition_cost_sar",
        "upfront_cash_exposure_sar",
        "payment_terms_days",
        "capacity_required_pct",
    }
)


class OfferEconomicsClass(StrEnum):
    PRODUCTIZED = "productized"
    MANAGED = "managed"
    RETAINER = "retainer"
    CUSTOM = "custom"


class FinancePricingStatus(StrEnum):
    DRAFT = "draft"
    FOUNDER_APPROVED = "founder_approved"


class CommercialFinanceDecision(StrEnum):
    PURSUE = "pursue"
    REVIEW = "review"
    STOP = "stop"


def _finite_decimal(
    value: Decimal | int | float | str,
    field_name: str,
    *,
    minimum: Decimal | None = None,
    maximum: Decimal | None = None,
) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError(f"{field_name} must be a decimal") from exc
    if not result.is_finite():
        raise ValueError(f"{field_name} must be finite")
    if minimum is not None and result < minimum:
        raise ValueError(f"{field_name} must be at least {minimum}")
    if maximum is not None and result > maximum:
        raise ValueError(f"{field_name} must be at most {maximum}")
    return result


def _money(value: Decimal) -> Decimal:
    return value.quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)


def _ratio(value: Decimal) -> Decimal:
    return value.quantize(RATIO_QUANTUM, rounding=ROUND_HALF_UP)


def _percent(value: Decimal) -> Decimal:
    return value.quantize(PERCENT_QUANTUM, rounding=ROUND_HALF_UP)


def _serialize(value: Any) -> Any:
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, StrEnum):
        return value.value
    if isinstance(value, tuple):
        return [_serialize(item) for item in value]
    if isinstance(value, Mapping):
        return {str(key): _serialize(item) for key, item in value.items()}
    return value


@dataclass(frozen=True)
class CommercialFinancePolicy:
    offer_class: OfferEconomicsClass
    gross_margin_floor: Decimal
    contribution_margin_floor: Decimal
    max_discount_pct: Decimal
    max_upfront_cash_exposure_sar: Decimal
    max_payment_terms_days: int
    max_capacity_required_pct: Decimal
    minimum_risk_adjusted_contribution_sar: Decimal = Decimal("0")
    minimum_probability_cohort_size: int = 5
    currency: str = "SAR"

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "gross_margin_floor",
            _finite_decimal(
                self.gross_margin_floor,
                "gross_margin_floor",
                minimum=Decimal("0"),
                maximum=Decimal("0.99"),
            ),
        )
        object.__setattr__(
            self,
            "contribution_margin_floor",
            _finite_decimal(
                self.contribution_margin_floor,
                "contribution_margin_floor",
                minimum=Decimal("0"),
                maximum=Decimal("0.99"),
            ),
        )
        object.__setattr__(
            self,
            "max_discount_pct",
            _finite_decimal(
                self.max_discount_pct,
                "max_discount_pct",
                minimum=Decimal("0"),
                maximum=Decimal("100"),
            ),
        )
        object.__setattr__(
            self,
            "max_upfront_cash_exposure_sar",
            _finite_decimal(
                self.max_upfront_cash_exposure_sar,
                "max_upfront_cash_exposure_sar",
                minimum=Decimal("0"),
            ),
        )
        object.__setattr__(
            self,
            "max_capacity_required_pct",
            _finite_decimal(
                self.max_capacity_required_pct,
                "max_capacity_required_pct",
                minimum=Decimal("0"),
                maximum=Decimal("100"),
            ),
        )
        object.__setattr__(
            self,
            "minimum_risk_adjusted_contribution_sar",
            _finite_decimal(
                self.minimum_risk_adjusted_contribution_sar,
                "minimum_risk_adjusted_contribution_sar",
            ),
        )
        if not 0 <= self.max_payment_terms_days <= 365:
            raise ValueError("max_payment_terms_days must be between 0 and 365")
        if self.minimum_probability_cohort_size < 1:
            raise ValueError("minimum_probability_cohort_size must be positive")
        if self.contribution_margin_floor > self.gross_margin_floor:
            raise ValueError("contribution margin floor cannot exceed gross margin floor")
        if not self.currency.strip() or len(self.currency) > 8:
            raise ValueError("currency must be a short non-empty code")


DEFAULT_POLICIES: dict[OfferEconomicsClass, CommercialFinancePolicy] = {
    OfferEconomicsClass.PRODUCTIZED: CommercialFinancePolicy(
        offer_class=OfferEconomicsClass.PRODUCTIZED,
        gross_margin_floor=Decimal("0.55"),
        contribution_margin_floor=Decimal("0.35"),
        max_discount_pct=Decimal("20"),
        max_upfront_cash_exposure_sar=Decimal("5000"),
        max_payment_terms_days=30,
        max_capacity_required_pct=Decimal("20"),
    ),
    OfferEconomicsClass.MANAGED: CommercialFinancePolicy(
        offer_class=OfferEconomicsClass.MANAGED,
        gross_margin_floor=Decimal("0.50"),
        contribution_margin_floor=Decimal("0.30"),
        max_discount_pct=Decimal("20"),
        max_upfront_cash_exposure_sar=Decimal("15000"),
        max_payment_terms_days=45,
        max_capacity_required_pct=Decimal("35"),
    ),
    OfferEconomicsClass.RETAINER: CommercialFinancePolicy(
        offer_class=OfferEconomicsClass.RETAINER,
        gross_margin_floor=Decimal("0.60"),
        contribution_margin_floor=Decimal("0.40"),
        max_discount_pct=Decimal("15"),
        max_upfront_cash_exposure_sar=Decimal("10000"),
        max_payment_terms_days=30,
        max_capacity_required_pct=Decimal("30"),
    ),
    OfferEconomicsClass.CUSTOM: CommercialFinancePolicy(
        offer_class=OfferEconomicsClass.CUSTOM,
        gross_margin_floor=Decimal("0.45"),
        contribution_margin_floor=Decimal("0.25"),
        max_discount_pct=Decimal("10"),
        max_upfront_cash_exposure_sar=Decimal("25000"),
        max_payment_terms_days=45,
        max_capacity_required_pct=Decimal("40"),
    ),
}


@dataclass(frozen=True)
class CommercialFinanceInputs:
    opportunity_id: str
    offer_id: str
    offer_class: OfferEconomicsClass
    list_price_sar: Decimal
    proposed_price_sar: Decimal
    delivery_cost_sar: Decimal
    acquisition_cost_sar: Decimal
    upfront_cash_exposure_sar: Decimal
    payment_terms_days: int
    capacity_required_pct: Decimal
    source_refs: Mapping[str, str]
    pricing_status: FinancePricingStatus = FinancePricingStatus.DRAFT
    close_probability_low: Decimal | None = None
    close_probability_base: Decimal | None = None
    close_probability_high: Decimal | None = None
    close_probability_source_ref: str | None = None
    close_probability_evidence_level: EvidenceLevel | None = None
    close_probability_cohort_size: int | None = None
    customer_roi_hypothesis_sar: Decimal | None = None
    customer_roi_source_ref: str | None = None

    def __post_init__(self) -> None:
        for field_name in ("opportunity_id", "offer_id"):
            value = getattr(self, field_name)
            if not value.strip() or len(value) > 64:
                raise ValueError(f"{field_name} must be 1-64 characters")
        for field_name in (
            "list_price_sar",
            "proposed_price_sar",
            "delivery_cost_sar",
            "acquisition_cost_sar",
            "upfront_cash_exposure_sar",
        ):
            object.__setattr__(
                self,
                field_name,
                _finite_decimal(getattr(self, field_name), field_name, minimum=Decimal("0")),
            )
        object.__setattr__(
            self,
            "capacity_required_pct",
            _finite_decimal(
                self.capacity_required_pct,
                "capacity_required_pct",
                minimum=Decimal("0"),
                maximum=Decimal("100"),
            ),
        )
        if self.list_price_sar <= 0 or self.proposed_price_sar <= 0:
            raise ValueError("list and proposed prices must be positive")
        if not 0 <= self.payment_terms_days <= 365:
            raise ValueError("payment_terms_days must be between 0 and 365")

        normalized_refs: dict[str, str] = {}
        if len(self.source_refs) > 32:
            raise ValueError("source_refs cannot contain more than 32 items")
        for key, value in self.source_refs.items():
            clean_key = str(key).strip()
            clean_value = str(value).strip()
            if not clean_key or len(clean_key) > 64:
                raise ValueError("source reference keys must be 1-64 characters")
            if not clean_value or len(clean_value) > 1000:
                raise ValueError("source reference values must be 1-1000 characters")
            normalized_refs[clean_key] = clean_value
        object.__setattr__(self, "source_refs", normalized_refs)

        probabilities = (
            self.close_probability_low,
            self.close_probability_base,
            self.close_probability_high,
        )
        supplied = [value is not None for value in probabilities]
        if any(supplied) and not all(supplied):
            raise ValueError("close probability low/base/high must be supplied together")
        if all(supplied):
            parsed = tuple(
                _finite_decimal(
                    value,
                    field_name,
                    minimum=Decimal("0"),
                    maximum=Decimal("1"),
                )
                for value, field_name in zip(
                    probabilities,
                    (
                        "close_probability_low",
                        "close_probability_base",
                        "close_probability_high",
                    ),
                    strict=True,
                )
            )
            if not parsed[0] <= parsed[1] <= parsed[2]:
                raise ValueError("close probabilities must be ordered low <= base <= high")
            object.__setattr__(self, "close_probability_low", parsed[0])
            object.__setattr__(self, "close_probability_base", parsed[1])
            object.__setattr__(self, "close_probability_high", parsed[2])
        if self.close_probability_source_ref is not None:
            clean_ref = self.close_probability_source_ref.strip()
            if not clean_ref or len(clean_ref) > 1000:
                raise ValueError("close_probability_source_ref must be 1-1000 characters")
            object.__setattr__(self, "close_probability_source_ref", clean_ref)
        if self.close_probability_cohort_size is not None and self.close_probability_cohort_size < 1:
            raise ValueError("close_probability_cohort_size must be positive")

        if self.customer_roi_hypothesis_sar is not None:
            object.__setattr__(
                self,
                "customer_roi_hypothesis_sar",
                _finite_decimal(
                    self.customer_roi_hypothesis_sar,
                    "customer_roi_hypothesis_sar",
                    minimum=Decimal("0"),
                ),
            )
            if not self.customer_roi_source_ref:
                raise ValueError("customer ROI hypothesis requires its own source reference")
        if self.customer_roi_source_ref is not None:
            clean_roi_ref = self.customer_roi_source_ref.strip()
            if not clean_roi_ref or len(clean_roi_ref) > 1000:
                raise ValueError("customer_roi_source_ref must be 1-1000 characters")
            object.__setattr__(self, "customer_roi_source_ref", clean_roi_ref)

    def to_dict(self) -> dict[str, Any]:
        return _serialize(
            {
                "opportunity_id": self.opportunity_id,
                "offer_id": self.offer_id,
                "offer_class": self.offer_class,
                "list_price_sar": self.list_price_sar,
                "proposed_price_sar": self.proposed_price_sar,
                "delivery_cost_sar": self.delivery_cost_sar,
                "acquisition_cost_sar": self.acquisition_cost_sar,
                "upfront_cash_exposure_sar": self.upfront_cash_exposure_sar,
                "payment_terms_days": self.payment_terms_days,
                "capacity_required_pct": self.capacity_required_pct,
                "source_refs": self.source_refs,
                "pricing_status": self.pricing_status,
                "close_probability_low": self.close_probability_low,
                "close_probability_base": self.close_probability_base,
                "close_probability_high": self.close_probability_high,
                "close_probability_source_ref": self.close_probability_source_ref,
                "close_probability_evidence_level": self.close_probability_evidence_level,
                "close_probability_cohort_size": self.close_probability_cohort_size,
                "customer_roi_hypothesis_sar": self.customer_roi_hypothesis_sar,
                "customer_roi_source_ref": self.customer_roi_source_ref,
            }
        )

    @classmethod
    def from_dict(
        cls,
        value: Mapping[str, Any],
        *,
        pricing_status: FinancePricingStatus | None = None,
    ) -> CommercialFinanceInputs:
        data = dict(value)
        data["offer_class"] = OfferEconomicsClass(data["offer_class"])
        data["pricing_status"] = pricing_status or FinancePricingStatus(
            data.get("pricing_status", FinancePricingStatus.DRAFT.value)
        )
        evidence_level = data.get("close_probability_evidence_level")
        data["close_probability_evidence_level"] = (
            EvidenceLevel(evidence_level) if evidence_level else None
        )
        return cls(**data)


@dataclass(frozen=True)
class CommercialFinanceAssessment:
    decision: CommercialFinanceDecision
    pricing_status: FinancePricingStatus
    currency: str
    readiness_score: int
    gross_profit_sar: Decimal
    gross_margin_pct: Decimal
    contribution_profit_sar: Decimal
    contribution_margin_pct: Decimal
    margin_floor_price_sar: Decimal
    discount_pct: Decimal
    discount_ceiling_price_sar: Decimal
    break_even_wins: int | None
    risk_adjusted_contribution_sar: Decimal
    expected_value_low_sar: Decimal | None
    expected_value_base_sar: Decimal | None
    expected_value_high_sar: Decimal | None
    expected_value_formula: str | None
    expected_value_evidence_eligible: bool
    customer_roi_hypothesis_sar: Decimal | None
    customer_roi_used_in_decision: bool
    blockers: tuple[str, ...]
    evidence_gaps: tuple[str, ...]
    warnings: tuple[str, ...]
    approval_required: bool = True
    external_action_allowed: bool = False

    @property
    def price_approved(self) -> bool:
        return self.pricing_status is FinancePricingStatus.FOUNDER_APPROVED

    def to_dict(self) -> dict[str, Any]:
        return _serialize(
            {
                "decision": self.decision,
                "pricing_status": self.pricing_status,
                "price_approved": self.price_approved,
                "currency": self.currency,
                "readiness_score": self.readiness_score,
                "gross_profit_sar": self.gross_profit_sar,
                "gross_margin_pct": self.gross_margin_pct,
                "contribution_profit_sar": self.contribution_profit_sar,
                "contribution_margin_pct": self.contribution_margin_pct,
                "margin_floor_price_sar": self.margin_floor_price_sar,
                "discount_pct": self.discount_pct,
                "discount_ceiling_price_sar": self.discount_ceiling_price_sar,
                "break_even_wins": self.break_even_wins,
                "risk_adjusted_contribution_sar": self.risk_adjusted_contribution_sar,
                "expected_value_low_sar": self.expected_value_low_sar,
                "expected_value_base_sar": self.expected_value_base_sar,
                "expected_value_high_sar": self.expected_value_high_sar,
                "expected_value_formula": self.expected_value_formula,
                "expected_value_evidence_eligible": self.expected_value_evidence_eligible,
                "customer_roi_hypothesis_sar": self.customer_roi_hypothesis_sar,
                "customer_roi_used_in_decision": self.customer_roi_used_in_decision,
                "blockers": self.blockers,
                "evidence_gaps": self.evidence_gaps,
                "warnings": self.warnings,
                "approval_required": self.approval_required,
                "external_action_allowed": self.external_action_allowed,
            }
        )


def policy_for_offer_class(offer_class: OfferEconomicsClass) -> CommercialFinancePolicy:
    return DEFAULT_POLICIES[offer_class]


def evaluate_commercial_finance(
    inputs: CommercialFinanceInputs,
    policy: CommercialFinancePolicy | None = None,
) -> CommercialFinanceAssessment:
    """Evaluate one immutable finance case without authorizing any action."""
    active_policy = policy or policy_for_offer_class(inputs.offer_class)
    if active_policy.offer_class is not inputs.offer_class:
        raise ValueError("finance policy offer class does not match the case")

    gross_profit = inputs.proposed_price_sar - inputs.delivery_cost_sar
    gross_margin = gross_profit / inputs.proposed_price_sar
    contribution_profit = gross_profit - inputs.acquisition_cost_sar
    contribution_margin = contribution_profit / inputs.proposed_price_sar
    gross_floor_price = inputs.delivery_cost_sar / (
        Decimal("1") - active_policy.gross_margin_floor
    )
    contribution_floor_price = (
        inputs.delivery_cost_sar + inputs.acquisition_cost_sar
    ) / (Decimal("1") - active_policy.contribution_margin_floor)
    margin_floor_price = max(gross_floor_price, contribution_floor_price)
    discount = (
        (inputs.list_price_sar - inputs.proposed_price_sar)
        / inputs.list_price_sar
        * Decimal("100")
    )
    discount_ceiling_price = inputs.list_price_sar * (
        Decimal("1") - active_policy.max_discount_pct / Decimal("100")
    )
    risk_adjusted_contribution = contribution_profit - inputs.upfront_cash_exposure_sar
    break_even_wins: int | None = None
    if gross_profit > 0:
        break_even_wins = int(
            (
                (inputs.upfront_cash_exposure_sar + inputs.acquisition_cost_sar)
                / gross_profit
            ).to_integral_value(rounding=ROUND_CEILING)
        )

    blockers: list[str] = []
    evidence_gaps: list[str] = []
    warnings: list[str] = []
    missing_source_refs = sorted(REQUIRED_ECONOMIC_SOURCE_KEYS - set(inputs.source_refs))
    evidence_gaps.extend(f"missing_source_ref:{key}" for key in missing_source_refs)

    if gross_profit <= 0:
        blockers.append("non_positive_gross_profit")
    if gross_margin < active_policy.gross_margin_floor:
        blockers.append("gross_margin_below_floor")
    if contribution_profit <= 0:
        blockers.append("non_positive_contribution_profit")
    if contribution_margin < active_policy.contribution_margin_floor:
        blockers.append("contribution_margin_below_floor")
    if inputs.proposed_price_sar < margin_floor_price:
        blockers.append("proposed_price_below_margin_floor")
    if discount > active_policy.max_discount_pct:
        blockers.append("discount_above_ceiling")
    if inputs.upfront_cash_exposure_sar > active_policy.max_upfront_cash_exposure_sar:
        blockers.append("upfront_cash_exposure_above_policy")
    if inputs.payment_terms_days > active_policy.max_payment_terms_days:
        blockers.append("payment_terms_above_policy")
    if inputs.capacity_required_pct > active_policy.max_capacity_required_pct:
        blockers.append("capacity_required_above_policy")
    if risk_adjusted_contribution < active_policy.minimum_risk_adjusted_contribution_sar:
        blockers.append("risk_adjusted_contribution_below_floor")
    if discount < 0:
        warnings.append("proposed_price_above_list_price")

    expected_values: tuple[Decimal | None, Decimal | None, Decimal | None] = (
        None,
        None,
        None,
    )
    expected_value_eligible = False
    probabilities_supplied = inputs.close_probability_low is not None
    if probabilities_supplied:
        if not inputs.close_probability_source_ref:
            evidence_gaps.append("close_probability_source_ref_required")
        if (
            inputs.close_probability_evidence_level is None
            or _EVIDENCE_RANK[inputs.close_probability_evidence_level]
            < _EVIDENCE_RANK[EvidenceLevel.L3_FIRST_PARTY]
        ):
            evidence_gaps.append("close_probability_requires_l3_first_party_evidence")
        if (
            inputs.close_probability_cohort_size is None
            or inputs.close_probability_cohort_size
            < active_policy.minimum_probability_cohort_size
        ):
            evidence_gaps.append("close_probability_cohort_below_minimum")
        expected_value_eligible = not any(
            gap.startswith("close_probability") for gap in evidence_gaps
        )
        if expected_value_eligible:
            expected_values = tuple(
                _money(probability * gross_profit - inputs.acquisition_cost_sar)
                for probability in (
                    inputs.close_probability_low,
                    inputs.close_probability_base,
                    inputs.close_probability_high,
                )
                if probability is not None
            )
            if expected_values[1] is not None and expected_values[1] < 0:
                blockers.append("base_expected_value_negative")
    else:
        warnings.append("expected_value_not_calculated_without_probability_evidence")

    if blockers:
        decision = CommercialFinanceDecision.STOP
    elif evidence_gaps:
        decision = CommercialFinanceDecision.REVIEW
    else:
        decision = CommercialFinanceDecision.PURSUE
    readiness_score = max(
        0,
        min(100, 100 - len(blockers) * 18 - len(evidence_gaps) * 8 - len(warnings) * 3),
    )

    return CommercialFinanceAssessment(
        decision=decision,
        pricing_status=inputs.pricing_status,
        currency=active_policy.currency,
        readiness_score=readiness_score,
        gross_profit_sar=_money(gross_profit),
        gross_margin_pct=_percent(gross_margin * Decimal("100")),
        contribution_profit_sar=_money(contribution_profit),
        contribution_margin_pct=_percent(contribution_margin * Decimal("100")),
        margin_floor_price_sar=_money(margin_floor_price),
        discount_pct=_percent(discount),
        discount_ceiling_price_sar=_money(discount_ceiling_price),
        break_even_wins=break_even_wins,
        risk_adjusted_contribution_sar=_money(risk_adjusted_contribution),
        expected_value_low_sar=expected_values[0],
        expected_value_base_sar=expected_values[1],
        expected_value_high_sar=expected_values[2],
        expected_value_formula=(
            "P(close) * gross_profit_if_won - acquisition_cost"
            if expected_value_eligible
            else None
        ),
        expected_value_evidence_eligible=expected_value_eligible,
        customer_roi_hypothesis_sar=(
            _money(inputs.customer_roi_hypothesis_sar)
            if inputs.customer_roi_hypothesis_sar is not None
            else None
        ),
        customer_roi_used_in_decision=False,
        blockers=tuple(dict.fromkeys(blockers)),
        evidence_gaps=tuple(dict.fromkeys(evidence_gaps)),
        warnings=tuple(dict.fromkeys(warnings)),
    )


__all__ = [
    "CommercialFinanceAssessment",
    "CommercialFinanceDecision",
    "CommercialFinanceInputs",
    "CommercialFinancePolicy",
    "DEFAULT_POLICIES",
    "FinancePricingStatus",
    "OfferEconomicsClass",
    "REQUIRED_ECONOMIC_SOURCE_KEYS",
    "evaluate_commercial_finance",
    "policy_for_offer_class",
]

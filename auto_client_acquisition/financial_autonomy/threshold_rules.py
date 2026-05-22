"""Threshold rule catalog for the financial autonomy cycle.

Codifies the financial guardrails that must trigger an approval or an
escalation. Every rule names a metric on
:class:`FinancialMetricsSnapshot`, a comparator, a threshold, and the
action that must be routed to the founder when the threshold is
breached.

Three documented rules cover irreversible operations that never expose
a metric on the snapshot (``refund_per_request``,
``price_change_significant``, ``write_off_significant``). They live in
this catalog so the founder approval routing stays in one place; the
``metric`` field is ``None`` for these documented-only rules.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from auto_client_acquisition.financial_autonomy.metrics_aggregator import (
    FinancialMetricsSnapshot,
)


Comparator = Literal["lt", "lte", "gt", "gte"]
Severity = Literal["low", "medium", "high", "critical"]
ActionOnViolation = Literal["flag", "approval_required", "escalate_board"]


@dataclass(frozen=True, slots=True)
class ThresholdRule:
    """A single financial guardrail."""

    rule_id: str
    source: str
    title_ar: str
    title_en: str
    metric: str | None
    comparator: Comparator
    threshold: float
    severity: Severity
    action_on_violation: ActionOnViolation
    reason_ar: str
    reason_en: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "source": self.source,
            "title_ar": self.title_ar,
            "title_en": self.title_en,
            "metric": self.metric,
            "comparator": self.comparator,
            "threshold": self.threshold,
            "severity": self.severity,
            "action_on_violation": self.action_on_violation,
            "reason_ar": self.reason_ar,
            "reason_en": self.reason_en,
        }


@dataclass(frozen=True, slots=True)
class ThresholdViolation:
    """A rule whose threshold has been breached by the current snapshot."""

    rule: ThresholdRule
    observed_value: float
    breached: bool
    action_on_violation: ActionOnViolation

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule": self.rule.to_dict(),
            "observed_value": self.observed_value,
            "breached": self.breached,
            "action_on_violation": self.action_on_violation,
        }


FINANCIAL_THRESHOLDS: tuple[ThresholdRule, ...] = (
    ThresholdRule(
        rule_id="gross_margin_floor",
        source="board_ready_os.financial_model:MIN_GROSS_MARGIN_PCT_FOR_SCALE",
        title_ar="حد أدنى للهامش الإجمالي",
        title_en="Gross margin floor",
        metric="gross_margin_pct",
        comparator="lt",
        threshold=35.0,
        severity="high",
        action_on_violation="approval_required",
        reason_ar="الهامش الإجمالي تحت 35% — لا توسعة قبل موافقة المؤسس.",
        reason_en="Gross margin below 35% — no scaling without founder approval.",
    ),
    ThresholdRule(
        rule_id="runway_critical",
        source="financial_autonomy.thresholds",
        title_ar="المدرّج الزمني حرج",
        title_en="Runway critical",
        metric="runway_months",
        comparator="lt",
        threshold=6.0,
        severity="critical",
        action_on_violation="escalate_board",
        reason_ar="مدرّج زمني أقل من 6 أشهر — تصعيد للمجلس.",
        reason_en="Runway under 6 months — escalate to the board.",
    ),
    ThresholdRule(
        rule_id="runway_warning",
        source="financial_autonomy.thresholds",
        title_ar="تحذير المدرّج الزمني",
        title_en="Runway warning",
        metric="runway_months",
        comparator="lt",
        threshold=12.0,
        severity="medium",
        action_on_violation="flag",
        reason_ar="مدرّج زمني أقل من 12 شهراً — راقب الحرق الشهري.",
        reason_en="Runway under 12 months — watch monthly burn.",
    ),
    ThresholdRule(
        rule_id="cac_payback_ceiling",
        source="financial_autonomy.thresholds",
        title_ar="سقف فترة استرداد CAC",
        title_en="CAC payback ceiling",
        metric="cac_payback_months",
        comparator="gt",
        threshold=12.0,
        severity="medium",
        action_on_violation="approval_required",
        reason_ar="استرداد CAC يتجاوز 12 شهراً — مراجعة قبل توسعة الاستحواذ.",
        reason_en="CAC payback exceeds 12 months — review before scaling acquisition.",
    ),
    ThresholdRule(
        rule_id="churn_spike",
        source="financial_autonomy.thresholds",
        title_ar="ارتفاع معدّل الانسحاب",
        title_en="Churn spike",
        metric="churn_pct_monthly",
        comparator="gt",
        threshold=10.0,
        severity="high",
        action_on_violation="approval_required",
        reason_ar="انسحاب شهري > 10% — أوقف الإنفاق على الاستحواذ.",
        reason_en="Monthly churn > 10% — pause acquisition spend.",
    ),
    ThresholdRule(
        rule_id="nrr_floor",
        source="financial_autonomy.thresholds",
        title_ar="حد أدنى لـ NRR",
        title_en="NRR floor",
        metric="nrr_pct",
        comparator="lt",
        threshold=90.0,
        severity="medium",
        action_on_violation="flag",
        reason_ar="NRR أقل من 90% — راجع نجاح العميل قبل أي توسعة.",
        reason_en="NRR below 90% — review customer success before scaling.",
    ),
    # Documented-only rules — no metric on the snapshot maps to these.
    # Routed through approvals when the underlying operation is requested.
    ThresholdRule(
        rule_id="refund_per_request",
        source="payment_ops.refund_state_machine",
        title_ar="استرداد فردي",
        title_en="Per-request refund",
        metric=None,
        comparator="gt",
        threshold=1000.0,
        severity="high",
        action_on_violation="approval_required",
        reason_ar="استرداد > 1,000 ر.س لكل طلب يتطلب موافقة المؤسس.",
        reason_en="Refund > 1,000 SAR per request requires founder approval.",
    ),
    ThresholdRule(
        rule_id="price_change_significant",
        source="financial_autonomy.thresholds",
        title_ar="تغيير سعر جوهري",
        title_en="Significant price change",
        metric=None,
        comparator="gt",
        threshold=5.0,
        severity="high",
        action_on_violation="approval_required",
        reason_ar="تغيير سعر > 5% يتطلب موافقة المؤسس + إشعار المجلس.",
        reason_en="Price change > 5% requires founder approval + board notice.",
    ),
)


def _get_metric(snapshot: FinancialMetricsSnapshot, name: str) -> float | None:
    value = getattr(snapshot, name, None)
    if value is None:
        return None
    try:
        return float(value)
    except Exception:  # noqa: BLE001
        return None


def _is_breached(value: float, comparator: Comparator, threshold: float) -> bool:
    if comparator == "lt":
        return value < threshold
    if comparator == "lte":
        return value <= threshold
    if comparator == "gt":
        return value > threshold
    if comparator == "gte":
        return value >= threshold
    return False


def evaluate_thresholds(
    snapshot: FinancialMetricsSnapshot,
) -> list[ThresholdViolation]:
    """Return the violations triggered by ``snapshot``.

    Documented-only rules (``metric`` is None) are skipped — they are
    raised by their owning operations (refunds, price changes), not by
    the metrics snapshot itself.
    """
    out: list[ThresholdViolation] = []
    for rule in FINANCIAL_THRESHOLDS:
        if rule.metric is None:
            continue
        value = _get_metric(snapshot, rule.metric)
        if value is None:
            continue
        breached = _is_breached(value, rule.comparator, rule.threshold)
        if not breached:
            continue
        out.append(
            ThresholdViolation(
                rule=rule,
                observed_value=round(value, 4),
                breached=True,
                action_on_violation=rule.action_on_violation,
            )
        )
    return out


__all__ = [
    "FINANCIAL_THRESHOLDS",
    "ThresholdRule",
    "ThresholdViolation",
    "evaluate_thresholds",
]

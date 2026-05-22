"""Financial anomaly detector — period-over-period comparison.

Compares the current :class:`FinancialMetricsSnapshot` against the
previous persisted snapshot and surfaces anomalies that warrant
founder review.

Kinds:
- ``revenue_regression``  — MRR dropped by more than 10%.
- ``churn_spike``         — churn rose by more than 5 pp.
- ``runway_dropped``      — runway dropped by more than 2 months.
- ``low_margin_emergence`` — gross margin fell from >=35% to <35%.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from auto_client_acquisition.financial_autonomy.metrics_aggregator import (
    FinancialMetricsSnapshot,
)


AnomalyKind = Literal[
    "revenue_regression",
    "churn_spike",
    "runway_dropped",
    "low_margin_emergence",
]
AnomalySeverity = Literal["low", "medium", "high", "critical"]


@dataclass(frozen=True, slots=True)
class Anomaly:
    """A single financial anomaly detected between two snapshots."""

    kind: AnomalyKind
    severity: AnomalySeverity
    evidence_ar: str
    evidence_en: str
    suggested_action_ar: str
    suggested_action_en: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "severity": self.severity,
            "evidence_ar": self.evidence_ar,
            "evidence_en": self.evidence_en,
            "suggested_action_ar": self.suggested_action_ar,
            "suggested_action_en": self.suggested_action_en,
        }


_REVENUE_REGRESSION_PCT = 10.0   # MRR dropped >10% MoM/WoW
_CHURN_SPIKE_DELTA = 5.0         # churn delta in percentage points
_RUNWAY_DROP_MONTHS = 2.0        # runway dropped >2 months
_MARGIN_FLOOR = 35.0             # margin fell to <35%


def _snapshot_field(
    snapshot: FinancialMetricsSnapshot | dict[str, Any] | None,
    name: str,
) -> float | None:
    if snapshot is None:
        return None
    if isinstance(snapshot, dict):
        value = snapshot.get(name)
    else:
        value = getattr(snapshot, name, None)
    if value is None:
        return None
    try:
        return float(value)
    except Exception:  # noqa: BLE001
        return None


def detect_anomalies(
    current: FinancialMetricsSnapshot | dict[str, Any],
    previous: FinancialMetricsSnapshot | dict[str, Any] | None = None,
) -> list[Anomaly]:
    """Return the list of anomalies between ``previous`` and ``current``.

    ``previous`` may be ``None`` (first-ever cycle) — in that case the
    detector returns an empty list, because there is no baseline to
    compare against. The signature accepts dicts too, so persisted
    snapshots can be passed directly.
    """
    if previous is None:
        return []
    out: list[Anomaly] = []

    prev_mrr = _snapshot_field(previous, "mrr_sar") or 0.0
    cur_mrr = _snapshot_field(current, "mrr_sar") or 0.0
    if prev_mrr > 0:
        change_pct = (cur_mrr - prev_mrr) / prev_mrr * 100.0
        if change_pct <= -_REVENUE_REGRESSION_PCT:
            out.append(
                Anomaly(
                    kind="revenue_regression",
                    severity="high",
                    evidence_ar=(
                        f"الإيراد الشهري انخفض من {prev_mrr:.0f} إلى "
                        f"{cur_mrr:.0f} ر.س ({change_pct:.1f}%)."
                    ),
                    evidence_en=(
                        f"MRR dropped from {prev_mrr:.0f} to {cur_mrr:.0f} SAR "
                        f"({change_pct:.1f}%)."
                    ),
                    suggested_action_ar="أوقف توسعة الاستحواذ وراجع أسباب الانخفاض.",
                    suggested_action_en="Pause acquisition expansion and review the drop.",
                )
            )

    prev_churn = _snapshot_field(previous, "churn_pct_monthly") or 0.0
    cur_churn = _snapshot_field(current, "churn_pct_monthly") or 0.0
    churn_delta = cur_churn - prev_churn
    if churn_delta > _CHURN_SPIKE_DELTA:
        out.append(
            Anomaly(
                kind="churn_spike",
                severity="high",
                evidence_ar=(
                    f"الانسحاب الشهري قفز من {prev_churn:.1f}% إلى "
                    f"{cur_churn:.1f}% (+{churn_delta:.1f} نقطة)."
                ),
                evidence_en=(
                    f"Monthly churn jumped from {prev_churn:.1f}% to "
                    f"{cur_churn:.1f}% (+{churn_delta:.1f} pp)."
                ),
                suggested_action_ar="نفّذ حملة احتفاظ مستهدفة قبل أي استحواذ جديد.",
                suggested_action_en="Run a targeted retention sweep before any new acquisition.",
            )
        )

    prev_runway = _snapshot_field(previous, "runway_months")
    cur_runway = _snapshot_field(current, "runway_months")
    if prev_runway is not None and cur_runway is not None:
        drop = prev_runway - cur_runway
        if drop > _RUNWAY_DROP_MONTHS:
            out.append(
                Anomaly(
                    kind="runway_dropped",
                    severity="high",
                    evidence_ar=(
                        f"المدرّج الزمني انخفض من {prev_runway:.1f} إلى "
                        f"{cur_runway:.1f} شهراً (-{drop:.1f})."
                    ),
                    evidence_en=(
                        f"Runway dropped from {prev_runway:.1f} to "
                        f"{cur_runway:.1f} months (-{drop:.1f})."
                    ),
                    suggested_action_ar="قلّل الحرق الشهري أو رتّب جولة تمويل.",
                    suggested_action_en="Cut monthly burn or line up a funding round.",
                )
            )

    prev_margin = _snapshot_field(previous, "gross_margin_pct")
    cur_margin = _snapshot_field(current, "gross_margin_pct")
    if (
        prev_margin is not None
        and cur_margin is not None
        and prev_margin >= _MARGIN_FLOOR
        and cur_margin < _MARGIN_FLOOR
    ):
        out.append(
            Anomaly(
                kind="low_margin_emergence",
                severity="high",
                evidence_ar=(
                    f"الهامش الإجمالي انخفض من {prev_margin:.1f}% إلى "
                    f"{cur_margin:.1f}% — أقل من 35%."
                ),
                evidence_en=(
                    f"Gross margin dropped from {prev_margin:.1f}% to "
                    f"{cur_margin:.1f}% — below 35%."
                ),
                suggested_action_ar="راجع تكلفة التسليم وأعد تسعير العروض ذات الهامش الضعيف.",
                suggested_action_en="Review delivery cost and reprice weak-margin offers.",
            )
        )

    return out


__all__ = ["Anomaly", "detect_anomalies"]

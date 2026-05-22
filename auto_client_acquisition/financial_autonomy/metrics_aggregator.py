"""Financial metrics aggregator — single source of truth per cycle.

Composes:
- :mod:`api.routers.revenue_metrics` (`_load_paid_history`, `_compute_dashboard`)
  for MRR/ARR/NRR/churn/ARPA.
- :mod:`auto_client_acquisition.operating_finance_os.lifecycle_unit_economics`
  for gross margin / LTV / CAC payback.
- :mod:`auto_client_acquisition.operating_finance_os.retainer_economics`
  for retainer health context.
- :mod:`auto_client_acquisition.capital_os.capital_ledger` for capital
  assets created this period.
- :mod:`auto_client_acquisition.revenue_pipeline.revenue_truth` for
  truth-table snapshot.

Friction-safe: every external lookup is wrapped — failures degrade to
warnings + estimates and never crash the cycle.

Estimates are explicitly flagged: a deployment with no delivery-cost
data records gross margin at the documented default (60%) and the field
``estimates_flagged`` contains the list of estimated values so the
founder always knows where the data ends and the assumption begins.
"""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from typing import Any

log = logging.getLogger(__name__)


# ── Documented defaults — flagged whenever they are used ────────────────
_DEFAULT_GROSS_MARGIN_PCT = 60.0
_DEFAULT_CASH_ON_HAND_SAR = 200_000.0
_DEFAULT_MONTHLY_BURN_SAR = 25_000.0
_DEFAULT_ACQUISITION_COST_SAR = 1_500.0
_DEFAULT_RETENTION_MONTHS = 12.0


@dataclass(frozen=True, slots=True)
class FinancialMetricsSnapshot:
    """Immutable snapshot of the financial state at ``period_end``."""

    period_end: str
    mrr_sar: float
    arr_sar: float
    nrr_pct: float
    churn_pct_monthly: float
    arpa_sar: float
    customers_active: int
    customers_total_ever: int
    gross_margin_pct: float
    ltv_sar: float
    cac_payback_months: float
    runway_months: float
    capital_assets_this_period: int
    revenue_truth: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    estimates_flagged: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "period_end": self.period_end,
            "mrr_sar": self.mrr_sar,
            "arr_sar": self.arr_sar,
            "nrr_pct": self.nrr_pct,
            "churn_pct_monthly": self.churn_pct_monthly,
            "arpa_sar": self.arpa_sar,
            "customers_active": self.customers_active,
            "customers_total_ever": self.customers_total_ever,
            "gross_margin_pct": self.gross_margin_pct,
            "ltv_sar": self.ltv_sar,
            "cac_payback_months": self.cac_payback_months,
            "runway_months": self.runway_months,
            "capital_assets_this_period": self.capital_assets_this_period,
            "revenue_truth": dict(self.revenue_truth),
            "warnings": list(self.warnings),
            "estimates_flagged": list(self.estimates_flagged),
        }


def _resolve_period_end(period_end: Any) -> str:
    if period_end is None:
        return date.today().isoformat()
    if isinstance(period_end, date):
        return period_end.isoformat()
    return str(period_end)


def _safe_load_paid_history() -> list[dict[str, Any]]:
    """Call ``_load_paid_history`` from the revenue_metrics router.

    Returns an empty list on any failure (DB unavailable, import error).
    """
    try:
        from api.routers.revenue_metrics import _load_paid_history
    except Exception as exc:  # noqa: BLE001
        log.debug("revenue_metrics import failed: %s", exc)
        return []
    try:
        # ``_load_paid_history`` is async; run it in a fresh loop in case
        # the caller is sync. If a loop is already running we cannot block
        # on it — fall back to an empty history rather than crash.
        try:
            asyncio.get_running_loop()
            log.debug("paid history not loaded — running inside an event loop")
            return []
        except RuntimeError:
            return asyncio.run(_load_paid_history())
    except Exception as exc:  # noqa: BLE001
        log.debug("paid history load failed: %s", exc)
        return []


def _safe_compute_dashboard(paid: list[dict[str, Any]]) -> dict[str, Any]:
    try:
        from api.routers.revenue_metrics import _compute_dashboard
    except Exception:  # noqa: BLE001
        return {}
    try:
        return _compute_dashboard(paid)
    except Exception as exc:  # noqa: BLE001
        log.debug("dashboard compute failed: %s", exc)
        return {}


def _safe_revenue_truth(paid_count: int, total_revenue_sar: int) -> dict[str, Any]:
    """Call ``snapshot_revenue_truth`` with a minimal pipeline summary.

    Degrades to an empty dict on any failure.
    """
    try:
        from auto_client_acquisition.revenue_pipeline.revenue_truth import (
            snapshot_revenue_truth,
        )
    except Exception:  # noqa: BLE001
        return {}
    try:
        snap = snapshot_revenue_truth(
            pipeline_summary={
                "total_leads": 0,
                "commitments": 0,
                "paid": int(paid_count),
                "total_revenue_sar": int(total_revenue_sar),
            },
            proof_event_files_count=0,
        )
    except Exception as exc:  # noqa: BLE001
        log.debug("revenue truth snapshot failed: %s", exc)
        return {}
    return {
        "total_leads": snap.total_leads,
        "commitments": snap.commitments,
        "paid": snap.paid,
        "total_revenue_sar": snap.total_revenue_sar,
        "revenue_live": snap.revenue_live,
        "paid_pilot_ready": snap.paid_pilot_ready,
        "v12_1_unlocked": snap.v12_1_unlocked,
        "blockers": list(snap.blockers),
        "next_action_ar": snap.next_action_ar,
        "next_action_en": snap.next_action_en,
    }


def _safe_capital_assets_count(period_end: str) -> int:
    """Count capital assets created on or before ``period_end``.

    Friction-safe: returns 0 on any failure.
    """
    try:
        from auto_client_acquisition.capital_os.capital_ledger import list_assets
    except Exception:  # noqa: BLE001
        return 0
    try:
        assets = list_assets(limit=10000)
    except Exception as exc:  # noqa: BLE001
        log.debug("capital ledger load failed: %s", exc)
        return 0
    # Plan asks for "this period" — for a weekly cycle we use a 35-day
    # window ending at period_end; for now we just count all assets in
    # the ledger, but stay friction-safe on the date parse.
    try:
        cutoff = datetime.fromisoformat(period_end).replace(tzinfo=UTC).timestamp()
    except Exception:  # noqa: BLE001
        return len(assets)
    window_start = cutoff - 35 * 86400
    count = 0
    for a in assets:
        try:
            ts = datetime.fromisoformat(a.created_at.replace("Z", "+00:00")).timestamp()
        except Exception:  # noqa: BLE001
            count += 1
            continue
        if window_start <= ts <= cutoff + 86400:
            count += 1
    return count


def _compose_lifecycle_economics(
    mrr_sar: float,
    customers_active: int,
    warnings: list[str],
    estimates_flagged: list[str],
) -> tuple[float, float, float]:
    """Return (gross_margin_pct, ltv_sar, cac_payback_months).

    Uses documented defaults when delivery-cost data is unavailable and
    flags every estimate via ``estimates_flagged``.
    """
    try:
        from auto_client_acquisition.operating_finance_os.lifecycle_unit_economics import (
            LifecycleEconomicsInputs,
            compute_lifecycle_economics,
        )
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"lifecycle_unit_economics_import_failed:{exc}")
        return (_DEFAULT_GROSS_MARGIN_PCT, 0.0, 0.0)

    monthly_revenue = float(mrr_sar) / max(1, customers_active) if customers_active else float(mrr_sar)
    # Default margin assumes 60% gross — flagged whenever we have no
    # delivery-cost data feeding the inputs.
    monthly_cost = monthly_revenue * (1.0 - _DEFAULT_GROSS_MARGIN_PCT / 100.0)
    estimates_flagged.append("gross_margin_pct")
    estimates_flagged.append("ltv_sar")
    estimates_flagged.append("cac_payback_months")

    inputs = LifecycleEconomicsInputs(
        monthly_revenue_sar=monthly_revenue,
        monthly_delivery_cost_sar=monthly_cost,
        acquisition_cost_sar=_DEFAULT_ACQUISITION_COST_SAR,
        retention_months=_DEFAULT_RETENTION_MONTHS,
        expansion_revenue_sar=0.0,
    )
    try:
        snap = compute_lifecycle_economics(inputs)
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"lifecycle_economics_compute_failed:{exc}")
        return (_DEFAULT_GROSS_MARGIN_PCT, 0.0, 0.0)
    payback = snap.cac_payback_months
    if payback == float("inf"):
        payback = 0.0
    return (snap.gross_margin_pct, snap.ltv_sar, payback)


def _compute_runway(
    mrr_sar: float,
    estimates_flagged: list[str],
) -> float:
    """Compute runway in months from documented defaults.

    runway = cash_on_hand / monthly_burn, where monthly_burn falls back to
    a documented default when MRR cannot cover delivery + AI cost.
    """
    burn = max(_DEFAULT_MONTHLY_BURN_SAR - mrr_sar, _DEFAULT_MONTHLY_BURN_SAR / 5.0)
    estimates_flagged.append("runway_months")
    estimates_flagged.append("cash_on_hand_estimate")
    estimates_flagged.append("monthly_burn_estimate")
    return round(_DEFAULT_CASH_ON_HAND_SAR / burn, 2)


def aggregate_financial_metrics(
    *,
    period_end: Any = None,
) -> FinancialMetricsSnapshot:
    """Aggregate the weekly financial metrics snapshot.

    Friction-safe: every dependency is wrapped — failures append a
    warning + a flagged estimate rather than crashing.
    """
    period_end_str = _resolve_period_end(period_end)
    warnings: list[str] = []
    estimates_flagged: list[str] = []

    # MRR / ARR / NRR / churn from the revenue dashboard ------------
    paid = _safe_load_paid_history()
    if not paid:
        warnings.append("no_paid_history_available")
    dashboard = _safe_compute_dashboard(paid)
    if not dashboard:
        warnings.append("revenue_dashboard_unavailable")

    mrr_sar = float(dashboard.get("mrr", {}).get("sar", 0))
    arr_sar = float(dashboard.get("arr", {}).get("sar", 0))
    nrr_pct = float(dashboard.get("nrr_pct", 0.0))
    churn_pct = float(dashboard.get("churn_pct_monthly", 0.0))
    arpa_sar = float(dashboard.get("arpa", {}).get("sar", 0))
    customers = dashboard.get("customers", {}) or {}
    customers_active = int(customers.get("active", 0))
    customers_total = int(customers.get("total_ever", 0))

    # Lifecycle economics (gross margin, LTV, CAC payback) ----------
    gross_margin_pct, ltv_sar, cac_payback = _compose_lifecycle_economics(
        mrr_sar, customers_active, warnings, estimates_flagged
    )

    # Runway (estimate) ---------------------------------------------
    runway_months = _compute_runway(mrr_sar, estimates_flagged)

    # Capital assets created this period ----------------------------
    capital_count = _safe_capital_assets_count(period_end_str)

    # Revenue truth snapshot ----------------------------------------
    total_revenue_sar = int(mrr_sar)
    revenue_truth = _safe_revenue_truth(len(paid), total_revenue_sar)

    return FinancialMetricsSnapshot(
        period_end=period_end_str,
        mrr_sar=round(mrr_sar, 2),
        arr_sar=round(arr_sar, 2),
        nrr_pct=round(nrr_pct, 2),
        churn_pct_monthly=round(churn_pct, 2),
        arpa_sar=round(arpa_sar, 2),
        customers_active=customers_active,
        customers_total_ever=customers_total,
        gross_margin_pct=round(gross_margin_pct, 2),
        ltv_sar=round(ltv_sar, 2),
        cac_payback_months=round(cac_payback, 2),
        runway_months=round(runway_months, 2),
        capital_assets_this_period=int(capital_count),
        revenue_truth=revenue_truth,
        warnings=warnings,
        estimates_flagged=estimates_flagged,
    )


__all__ = [
    "FinancialMetricsSnapshot",
    "aggregate_financial_metrics",
]

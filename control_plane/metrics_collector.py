"""MetricsCollector: build a CompanyState snapshot from inputs.

This is the boundary into the control plane. In production it would read from
the database, CRM, billing, and CI. For the doctrine layer we keep it pure:
callers pass a dict and we return a typed CompanyState. No I/O.
"""

from __future__ import annotations

from typing import Any, Dict

from control_plane.company_state import (
    ClientSuccessState,
    CompanyState,
    DeliveryState,
    FinanceState,
    ProductState,
    RevenueState,
    SalesState,
    TrustState,
)


def _get(d: Dict[str, Any], key: str, default: Any) -> Any:
    if not isinstance(d, dict):
        return default
    val = d.get(key, default)
    return default if val is None else val


class MetricsCollector:
    """Map an untyped metrics dict to a typed CompanyState."""

    def collect(self, raw: Dict[str, Any]) -> CompanyState:
        revenue = _get(raw, "revenue", {})
        sales = _get(raw, "sales", {})
        delivery = _get(raw, "delivery", {})
        trust = _get(raw, "trust", {})
        product = _get(raw, "product", {})
        finance = _get(raw, "finance", {})
        client_success = _get(raw, "client_success", {})

        return CompanyState(
            revenue=RevenueState(
                cash_collected=float(_get(revenue, "cash_collected", 0.0)),
                cash_expected=float(_get(revenue, "cash_expected", 0.0)),
                mrr=float(_get(revenue, "mrr", 0.0)),
                proposals_pending=int(_get(revenue, "proposals_pending", 0)),
                pipeline_value=float(_get(revenue, "pipeline_value", 0.0)),
                best_next_close=_get(revenue, "best_next_close", None),
            ),
            sales=SalesState(
                leads_new=int(_get(sales, "leads_new", 0)),
                dms_due=int(_get(sales, "dms_due", 0)),
                followups_due=int(_get(sales, "followups_due", 0)),
                replies=int(_get(sales, "replies", 0)),
                calls_booked=int(_get(sales, "calls_booked", 0)),
            ),
            delivery=DeliveryState(
                active_clients=int(_get(delivery, "active_clients", 0)),
                reports_due=int(_get(delivery, "reports_due", 0)),
                blocked_deliveries=int(_get(delivery, "blocked_deliveries", 0)),
                qa_needed=int(_get(delivery, "qa_needed", 0)),
            ),
            trust=TrustState(
                approvals_waiting=int(_get(trust, "approvals_waiting", 0)),
                a3_blocked_actions=int(_get(trust, "a3_blocked_actions", 0)),
                opt_outs=int(_get(trust, "opt_outs", 0)),
                claims_needing_review=int(_get(trust, "claims_needing_review", 0)),
                incidents=int(_get(trust, "incidents", 0)),
            ),
            product=ProductState(
                ci_status=str(_get(product, "ci_status", "unknown")),
                bugs_open=int(_get(product, "bugs_open", 0)),
                customer_requested_features=int(
                    _get(product, "customer_requested_features", 0)
                ),
                release_candidate=_get(product, "release_candidate", None),
            ),
            finance=FinanceState(
                runway_months=_get(finance, "runway_months", None),
                refunds_open=int(_get(finance, "refunds_open", 0)),
                invoices_overdue=int(_get(finance, "invoices_overdue", 0)),
            ),
            client_success=ClientSuccessState(
                health_below_60=int(_get(client_success, "health_below_60", 0)),
                retainer_ready=int(_get(client_success, "retainer_ready", 0)),
                feedback_collected=int(_get(client_success, "feedback_collected", 0)),
            ),
            decisions_required=list(_get(raw, "decisions_required", [])),
            alerts=list(_get(raw, "alerts", [])),
        )

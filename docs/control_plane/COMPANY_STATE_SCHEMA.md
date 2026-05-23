# CompanyState Schema

`CompanyState` is the single typed view of Dealix at a point in time.

## Top-level fields

| Field | Type | Source |
|---|---|---|
| `as_of` | ISO date string | Collector default = today |
| `revenue` | `RevenueState` | Billing + pipeline |
| `sales` | `SalesState` | CRM + outreach ledger |
| `delivery` | `DeliveryState` | Client tracker |
| `trust` | `TrustState` | Approval log + incident log |
| `product` | `ProductState` | CI + issue tracker |
| `finance` | `FinanceState` | Bank + invoicing |
| `client_success` | `ClientSuccessState` | Health score system |
| `decisions_required` | list of dicts | Decision Engine outputs |
| `alerts` | list of dicts | CEO Alerts engine |

## RevenueState
- `cash_collected: float`
- `cash_expected: float`
- `mrr: float`
- `proposals_pending: int`
- `pipeline_value: float`
- `best_next_close: str | None`

## SalesState
- `leads_new`, `dms_due`, `followups_due`, `replies`, `calls_booked` (int)

## DeliveryState
- `active_clients`, `reports_due`, `blocked_deliveries`, `qa_needed` (int)

## TrustState
- `approvals_waiting`, `a3_blocked_actions`, `opt_outs`,
  `claims_needing_review`, `incidents` (int)

## ProductState
- `ci_status: str` (e.g. "green", "red", "unknown")
- `bugs_open: int`
- `customer_requested_features: int`
- `release_candidate: str | None`

## FinanceState
- `runway_months: float | None`
- `refunds_open: int`
- `invoices_overdue: int`

## ClientSuccessState
- `health_below_60: int`
- `retainer_ready: int`
- `feedback_collected: int`

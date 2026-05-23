"""CEO Brief Engine: render a Daily Command Brief from CompanyState."""

from __future__ import annotations

from datetime import date
from typing import List, Optional

from control_plane.company_state import CompanyState


def _fmt_money(v: float) -> str:
    return f"{v:,.0f} SAR"


def _maybe(v) -> str:
    return "—" if v is None or v == "" else str(v)


def render_daily_brief(
    state: CompanyState,
    focus: Optional[str] = None,
    kill_or_defer: Optional[List[str]] = None,
) -> str:
    """Render a Markdown daily brief from the given CompanyState."""

    decisions_md = "| Decision | Type | Risk | Recommendation |\n|---|---|---:|---|"
    for d in state.decisions_required:
        decisions_md += (
            f"\n| {d.get('decision','—')} | {d.get('type','—')} | "
            f"{d.get('risk','—')} | {d.get('recommendation','—')} |"
        )
    if not state.decisions_required:
        decisions_md += "\n| — | — | — | — |"

    kd = "\n".join(f"- {x}" for x in (kill_or_defer or [])) or "-"

    return f"""# Daily CEO Brief

## Date
{state.as_of or date.today().isoformat()}

## One Focus Today
{focus or "—"}

## Revenue
- Cash collected: {_fmt_money(state.revenue.cash_collected)}
- Cash expected: {_fmt_money(state.revenue.cash_expected)}
- MRR: {_fmt_money(state.revenue.mrr)}
- Proposals pending: {state.revenue.proposals_pending}
- Pipeline value: {_fmt_money(state.revenue.pipeline_value)}
- Best next close: {_maybe(state.revenue.best_next_close)}

## Sales
- New leads: {state.sales.leads_new}
- DMs due: {state.sales.dms_due}
- Follow-ups due: {state.sales.followups_due}
- Replies: {state.sales.replies}
- Calls booked: {state.sales.calls_booked}

## Delivery
- Active clients: {state.delivery.active_clients}
- Reports due: {state.delivery.reports_due}
- Blocked deliveries: {state.delivery.blocked_deliveries}
- QA needed: {state.delivery.qa_needed}

## Trust
- Approvals waiting: {state.trust.approvals_waiting}
- A3 blocked actions: {state.trust.a3_blocked_actions}
- Opt-outs: {state.trust.opt_outs}
- Claims needing review: {state.trust.claims_needing_review}
- Incidents: {state.trust.incidents}

## Product
- CI status: {state.product.ci_status}
- Bugs open: {state.product.bugs_open}
- Customer-requested features: {state.product.customer_requested_features}
- Release candidate: {_maybe(state.product.release_candidate)}

## Decisions Required
{decisions_md}

## Kill / Defer Today
{kd}

## End-of-Day Result
-
"""

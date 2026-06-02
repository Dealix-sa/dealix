#!/usr/bin/env python3
"""Verify the Recurring Revenue Radar invariants (CI gate).

Deterministic self-check that the portfolio expansion scanner honours its three
non-negotiables on a known synthetic portfolio:
  * proof before upsell (ineligible accounts are never opportunities),
  * no revenue before paid (unpaid current MRR excluded from realised + baseline),
  * approval-first (every action is draft_only / requires_approval).

Prints ``RECURRING_REVENUE_RADAR_VERIFY=PASS`` and exits 0 on success.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.revenue_ops_autopilot.recurring_revenue_radar import (  # noqa: E402
    RETAINER_TIER_MRR_SAR,
    run_radar,
)
from dealix.revenue_ops_autopilot.retainer_eligibility import RetainerTier  # noqa: E402

_PORTFOLIO = [
    {"account_id": "scale", "company_name": "Scale Co", "proof_level": "L3",
     "satisfaction_score": 9.0, "measurable_result_achieved": True},
    {"account_id": "growth", "company_name": "Growth Co", "proof_level": "L2",
     "satisfaction_score": 8.0, "measurable_result_achieved": True},
    {"account_id": "starter", "company_name": "Starter Co", "proof_level": "L1",
     "satisfaction_score": 7.0, "measurable_result_achieved": True},
    {"account_id": "unpaid", "company_name": "Unpaid Co", "proof_level": "L2",
     "satisfaction_score": 8.0, "measurable_result_achieved": True,
     "current_mrr_sar": 2999.0, "latest_invoice_paid": False},
    {"account_id": "ineligible", "company_name": "Ineligible Co", "proof_level": "L0",
     "satisfaction_score": 5.0, "measurable_result_achieved": False},
]


def main() -> int:
    failures: list[str] = []
    summary = run_radar(_PORTFOLIO)

    # Tier price map must never drift from the tier identifiers.
    if set(RETAINER_TIER_MRR_SAR) != set(RetainerTier.__args__):  # type: ignore[attr-defined]
        failures.append("tier_mrr_map_out_of_sync")
    for tier, mrr in RETAINER_TIER_MRR_SAR.items():
        if not tier.endswith(str(mrr)):
            failures.append(f"tier_price_drift:{tier}")

    by_id = {o.account_id: o for o in summary.opportunities}

    # proof before upsell
    if by_id["ineligible"].is_expansion_opportunity:
        failures.append("ineligible_account_marked_opportunity")

    # no revenue before paid
    if summary.realized_mrr_sar != 0.0:
        failures.append(f"unpaid_counted_as_realised:{summary.realized_mrr_sar}")
    if by_id["unpaid"].current_mrr_sar != 0.0:
        failures.append("unpaid_current_mrr_in_baseline")

    # tiers + ranking
    if by_id["scale"].recommended_tier != "scale_4999":
        failures.append("scale_tier_wrong")
    # "unpaid" ties "growth" at +3,999 (its unpaid 2,999 is excluded from the
    # baseline) and sorts before it only by account_id — both rank above starter.
    ranked = [o.account_id for o in summary.opportunities if o.is_expansion_opportunity]
    if ranked != ["scale", "growth", "unpaid", "starter"]:
        failures.append(f"ranking_wrong:{ranked}")

    # approval-first
    for opp in summary.opportunities:
        if not opp.requires_approval or opp.mode != "draft_only":
            failures.append(f"not_draft_only:{opp.account_id}")

    expected_pipeline = 4999 + 3999 + 2999 + 3999  # scale+growth+starter+unpaid(zero baseline)
    if summary.pipeline_incremental_mrr_sar != expected_pipeline:
        failures.append(
            f"pipeline_total_wrong:{summary.pipeline_incremental_mrr_sar}!={expected_pipeline}"
        )

    if failures:
        print("RECURRING_REVENUE_RADAR_VERIFY=FAIL")
        for f in failures:
            print(f"- {f}")
        return 1

    print(
        f"accounts={summary.accounts_total} opportunities={summary.opportunities_count} "
        f"pipeline_mrr={summary.pipeline_incremental_mrr_sar:,.0f} SAR "
        f"pipeline_arr={summary.pipeline_incremental_arr_sar:,.0f} SAR"
    )
    print("RECURRING_REVENUE_RADAR_VERIFY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

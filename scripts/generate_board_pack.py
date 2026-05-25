import argparse
import sys
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ops_runtime.business_audit import calculate_business_score
from ops_runtime.finance_calculator import calculate_finance


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()
    root = Path(args.private_ops).resolve()
    score = calculate_business_score(str(root))
    finance = calculate_finance(str(root))
    metrics = score["metrics"]
    content = f"""# Dealix Monthly Board Pack

## Date
{date.today().isoformat()}

## 1. Executive Summary
Dealix is currently at **{score['status']}** with CEO Business Score **{score['total_score']} / 100**.

## 2. CEO Business Score
| Area | Score |
|---|---:|
| Revenue Execution | {score['revenue_score']} / 20 |
| Sales Pipeline | {score['pipeline_score']} / 15 |
| Financial Control | {score['finance_score']} / 15 |
| Delivery Readiness | {score['delivery_score']} / 15 |
| Trust & AI Governance | {score['trust_score']} / 10 |
| Learning System | {score['learning_score']} / 10 |
| CEO Cadence | {score['ceo_score']} / 10 |
| Product Discipline | {score['product_score']} / 5 |

## 3. Revenue
| Metric | Value |
|---|---:|
| Leads | {metrics['lead_count']} |
| Contacted | {metrics['contacted']} |
| Replies | {metrics['replied']} |
| Samples Sent | {metrics['sample_sent']} |
| Proposals Sent | {metrics['proposal_sent']} |
| Paid | {metrics['paid']} |
| Cash Collected | {metrics['cash_collected']} SAR |
| Pipeline Value | {metrics['pipeline_value']} SAR |
| MRR | {metrics['mrr']} SAR |

## 4. Finance
| Metric | Value |
|---|---:|
| Cash Collected | {finance['cash_collected']} SAR |
| Pipeline Value | {finance['pipeline_value']} SAR |
| Weighted Pipeline | {finance['weighted_pipeline']} SAR |
| MRR | {finance['mrr']} SAR |
| Monthly Expenses | {finance['monthly_expenses']} SAR |
| Net Burn | {finance['net_burn']} SAR |

## 5. Delivery
- Delivered: {metrics['delivered']}
- Retainers: {metrics['retainer']}
- Delivery QA: Review delivery/qa and client reports.

## 6. Trust & AI Governance
- Review approval_log.csv.
- Confirm no A3 actions executed.
- Confirm no public/private boundary failures.
- Confirm AI outputs remain assisted, not autonomous.

## 7. Learning
- Review weekly_reviews.
- Confirm one learning decision per week.
- Confirm one system update per week.

## 8. Productization
- Review learning/productization_candidates.md.
- Productize only repeated workflows.

## 9. Key Risks
- No first paid sprint.
- Founder distraction.
- Overbuilding before proof.
- Weak delivery proof.
- Trust incident from overclaims or unsafe automation.

## 10. CEO Decisions Needed
1. Build / Fix / Kill / Defer decision:
2. Next month focus:
3. System to improve:
4. Initiative to kill/defer:

## 11. Next Action
{score['next_action']}
"""
    out_dir = root / "founder"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "monthly_board_pack.md"
    out.write_text(content, encoding="utf-8")
    print(f"PASS: wrote board pack to {out}")


if __name__ == "__main__":
    main()

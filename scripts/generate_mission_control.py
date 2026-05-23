import argparse
import sys
from pathlib import Path
from datetime import date

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from ops_runtime.business_audit import calculate_business_score
from ops_runtime.finance_calculator import calculate_finance
from ops_runtime.execution_assurance import calculate_execution_assurance
from control_plane.control_tower import build_control_tower_signal
from control_plane.strategic_decision_engine import recommend_strategic_decision
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()
    root = Path(args.private_ops).resolve()
    score = calculate_business_score(str(root))
    finance = calculate_finance(str(root))
    assurance = calculate_execution_assurance(str(root))
    tower = build_control_tower_signal(score)
    decision = recommend_strategic_decision(score)
    metrics = score["metrics"]
    content = f"""# Dealix Mission Control
## Date
{date.today().isoformat()}
## Company Posture
{tower['posture']}
## Top CEO Action
{tower['top_action']}
## Strategic Decision
{decision['decision']} — {decision['area']}
## Strategic Action
{decision['action']}
## Business Score
{score['total_score']} / 100
## Execution Assurance
{assurance['score']} / 100 — {assurance['status']}
## Finance
- Cash collected: {finance['cash_collected']} SAR
- Pipeline value: {finance['pipeline_value']} SAR
- Weighted pipeline: {finance['weighted_pipeline']} SAR
- MRR: {finance['mrr']} SAR
- Monthly expenses: {finance['monthly_expenses']} SAR
- Net burn: {finance['net_burn']} SAR
## Revenue Reality
- Leads: {metrics['lead_count']}
- Contacted: {metrics['contacted']}
- Replies: {metrics['replied']}
- Samples sent: {metrics['sample_sent']}
- Proposals sent: {metrics['proposal_sent']}
- Paid: {metrics['paid']}
- Cash collected: {metrics['cash_collected']} SAR
## Delivery Reality
- Delivered: {metrics['delivered']}
- Retainers: {metrics['retainer']}
## Trust Reality
Review trust/approval_log.csv and founder/approvals_waiting.md.
## One Action Before Anything Else
{tower['top_action']}
## CEO Rule
Do not build, polish, or expand before completing the top action.
"""
    out = root / "founder/mission_control.md"
    out.write_text(content, encoding="utf-8")
    print("PASS: Mission Control generated.")
    print(f"Top action: {tower['top_action']}")
    print(f"Written: {out}")
if __name__ == "__main__":
    main()

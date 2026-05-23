"""Generate the CEO Business Score markdown and append to history CSV.

Usage:
    python scripts/generate_ceo_business_score.py --private-ops /path/to/dealix-ops-private
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

# Allow running from repo root without installing the package.
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops_runtime.business_audit import calculate_business_score


HISTORY_HEADERS = [
    "date",
    "total_score",
    "revenue_score",
    "pipeline_score",
    "finance_score",
    "delivery_score",
    "trust_score",
    "learning_score",
    "ceo_score",
    "product_score",
    "status",
    "next_action",
]


def write_score_markdown(root: Path, score: dict) -> Path:
    metrics = score["metrics"]
    content = f"""# CEO Business Score

## Date
{score['date']}

## Total Score
{score['total_score']} / 100

## Status
{score['status']}

## Next Action
{score['next_action']}

## Score Breakdown
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

## Core Metrics
| Metric | Value |
|---|---:|
| Leads | {metrics['lead_count']} |
| Contacted | {metrics['contacted']} |
| Replies | {metrics['replied']} |
| Samples Sent | {metrics['sample_sent']} |
| Proposals Sent | {metrics['proposal_sent']} |
| Paid | {metrics['paid']} |
| Delivered | {metrics['delivered']} |
| Retainers | {metrics['retainer']} |
| Cash Collected | {metrics['cash_collected']} SAR |
| Pipeline Value | {metrics['pipeline_value']} SAR |
| MRR | {metrics['mrr']} SAR |
| Monthly Expenses | {metrics['monthly_expenses']} SAR |

## CEO Interpretation
- If score is below 50: complete setup gaps.
- If score is 50–74: fix execution before scale.
- If score is 75–89: execute market push.
- If score is 90+: operate, deliver, and retain.

## CEO Rule
Do not expand product scope until Revenue Sprint evidence exists.
"""
    out = root / "business_audit/ceo_business_score.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    return out


def append_history(root: Path, score: dict) -> Path:
    path = root / "business_audit/score_history.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists() and path.stat().st_size > 0
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HISTORY_HEADERS)
        if not exists:
            writer.writeheader()
        writer.writerow({key: score.get(key, "") for key in HISTORY_HEADERS})
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-ops", required=True, help="Path to dealix-ops-private root.")
    args = parser.parse_args()

    root = Path(args.private_ops).resolve()
    if not root.exists():
        raise SystemExit(f"private-ops path does not exist: {root}")

    score = calculate_business_score(str(root))
    md = write_score_markdown(root, score)
    history = append_history(root, score)

    print("PASS: CEO Business Score generated.")
    print(f"Score: {score['total_score']} / 100")
    print(f"Status: {score['status']}")
    print(f"Next action: {score['next_action']}")
    print(f"Written: {md}")
    print(f"History: {history}")


if __name__ == "__main__":
    main()

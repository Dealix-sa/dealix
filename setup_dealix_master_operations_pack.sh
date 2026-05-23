#!/usr/bin/env bash
set -euo pipefail

echo "== Dealix Master Operations Pack =="

mkdir -p ops_runtime scripts

touch ops_runtime/__init__.py
touch ops_runtime/private_ops_reader.py
touch ops_runtime/metrics_calculator.py
touch ops_runtime/ceo_brief_generator.py
touch ops_runtime/weekly_review_generator.py
touch ops_runtime/bottleneck_analyzer.py
touch ops_runtime/scorecard_updater.py
touch ops_runtime/decision_queue_builder.py
touch ops_runtime/markdown_writer.py

cat > ops_runtime/private_ops_reader.py <<'PY'
from pathlib import Path
import csv


class PrivateOpsReader:
    def __init__(self, private_ops_path: str):
        self.root = Path(private_ops_path)

    def read_csv(self, relative_path: str):
        path = self.root / relative_path
        if not path.exists():
            return []
        with path.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def read_text(self, relative_path: str) -> str:
        path = self.root / relative_path
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")

    def exists(self, relative_path: str) -> bool:
        return (self.root / relative_path).exists()
PY

cat > ops_runtime/metrics_calculator.py <<'PY'
from collections import Counter


def calculate_pipeline_metrics(pipeline_rows):
    stages = Counter((row.get("stage") or "Unknown").strip() for row in pipeline_rows)

    return {
        "lead_count": len(pipeline_rows),
        "new": stages.get("New", 0),
        "qualified": stages.get("Qualified", 0),
        "contacted": stages.get("Contacted", 0),
        "replied": stages.get("Replied", 0),
        "sample_sent": stages.get("Sample Sent", 0),
        "call_booked": stages.get("Call Booked", 0),
        "proposal_sent": stages.get("Proposal Sent", 0),
        "paid": stages.get("Paid", 0),
        "delivered": stages.get("Delivered", 0),
        "retainer": stages.get("Retainer", 0),
        "lost": stages.get("Lost", 0),
    }


def calculate_mrr_metrics(mrr_rows):
    active = [
        row for row in mrr_rows
        if (row.get("status") or "").strip().lower() in {"active", "paid", "current"}
    ]

    total_mrr = 0.0
    for row in active:
        try:
            total_mrr += float(row.get("monthly_amount") or 0)
        except ValueError:
            pass

    return {
        "active_retainers": len(active),
        "mrr": total_mrr,
    }


def calculate_approval_metrics(approval_rows):
    pending = [
        row for row in approval_rows
        if (row.get("decision") or "").strip().lower() in {"pending", ""}
    ]

    high_risk = [
        row for row in approval_rows
        if (row.get("risk_level") or "").strip().lower() in {"high", "critical"}
    ]

    return {
        "approvals_total": len(approval_rows),
        "approvals_pending": len(pending),
        "high_risk_approvals": len(high_risk),
    }
PY

cat > ops_runtime/bottleneck_analyzer.py <<'PY'
def analyze_bottlenecks(metrics):
    bottlenecks = []

    if metrics.get("lead_count", 0) < 25:
        bottlenecks.append({
            "area": "Sales",
            "severity": "High",
            "issue": "Lead volume below weekly target.",
            "recommendation": "Add at least 25 qualified leads to pipeline."
        })

    if metrics.get("contacted", 0) < 25:
        bottlenecks.append({
            "area": "Acquisition",
            "severity": "High",
            "issue": "Outbound volume below weekly target.",
            "recommendation": "Send first 25 founder-led DMs."
        })

    if metrics.get("proposal_sent", 0) == 0 and metrics.get("replied", 0) > 0:
        bottlenecks.append({
            "area": "Sales",
            "severity": "Medium",
            "issue": "Replies exist but no proposals sent.",
            "recommendation": "Qualify replies and send at least one proposal."
        })

    if metrics.get("paid", 0) == 0 and metrics.get("proposal_sent", 0) > 0:
        bottlenecks.append({
            "area": "Revenue",
            "severity": "High",
            "issue": "Proposals sent but no payments recorded.",
            "recommendation": "Improve payment path, urgency, and follow-up."
        })

    if metrics.get("approvals_pending", 0) > 5:
        bottlenecks.append({
            "area": "Founder",
            "severity": "Medium",
            "issue": "Too many approvals waiting.",
            "recommendation": "Batch approvals daily and clarify approval matrix."
        })

    return bottlenecks
PY

cat > ops_runtime/ceo_brief_generator.py <<'PY'
from datetime import date


def generate_ceo_brief(metrics, bottlenecks):
    top_focus = "Send 25 founder-led DMs and prepare 3 samples."

    if bottlenecks:
        top = bottlenecks[0]
        top_focus = f"{top['recommendation']}"

    bottleneck_lines = "\n".join(
        f"- **{b['area']} / {b['severity']}**: {b['issue']} → {b['recommendation']}"
        for b in bottlenecks
    ) or "- No major bottlenecks detected."

    return f"""# Daily CEO Brief

## Date
{date.today().isoformat()}

## One CEO Focus Today
{top_focus}

## Money
- MRR: {metrics.get('mrr', 0)}
- Active retainers: {metrics.get('active_retainers', 0)}
- Paid opportunities: {metrics.get('paid', 0)}
- Proposals sent: {metrics.get('proposal_sent', 0)}

## Sales
- Lead count: {metrics.get('lead_count', 0)}
- New: {metrics.get('new', 0)}
- Contacted: {metrics.get('contacted', 0)}
- Replied: {metrics.get('replied', 0)}
- Calls booked: {metrics.get('call_booked', 0)}
- Samples sent: {metrics.get('sample_sent', 0)}

## Delivery
- Delivered: {metrics.get('delivered', 0)}
- Retainers: {metrics.get('retainer', 0)}

## Trust
- Approvals total: {metrics.get('approvals_total', 0)}
- Approvals pending: {metrics.get('approvals_pending', 0)}
- High-risk approvals: {metrics.get('high_risk_approvals', 0)}

## Bottlenecks
{bottleneck_lines}

## Decisions Required
| Decision | Type | Risk | Recommendation |
|---|---|---:|---|
| Review top bottleneck | Fix | Medium | {top_focus} |

## End-of-Day Result
-
"""
PY

cat > ops_runtime/weekly_review_generator.py <<'PY'
from datetime import date


def generate_weekly_review(metrics, bottlenecks):
    bottleneck_lines = "\n".join(
        f"- {b['area']}: {b['issue']} → {b['recommendation']}"
        for b in bottlenecks
    ) or "- No major bottlenecks detected."

    return f"""# Weekly Intelligence Review

## Week Ending
{date.today().isoformat()}

## What Happened?
- Leads sourced: {metrics.get('lead_count', 0)}
- Contacted: {metrics.get('contacted', 0)}
- Replies: {metrics.get('replied', 0)}
- Calls booked: {metrics.get('call_booked', 0)}
- Proposals sent: {metrics.get('proposal_sent', 0)}
- Paid: {metrics.get('paid', 0)}
- Delivered: {metrics.get('delivered', 0)}
- Retainers: {metrics.get('retainer', 0)}

## What Worked?
- Best visible signal: Update after reviewing replies and calls.

## What Failed?
- Review weak conversion points.

## Bottlenecks
{bottleneck_lines}

## Learning Decision
| Learning | Decision | Update Needed |
|---|---|---|
| Weekly bottleneck review | Fix highest bottleneck | Update relevant playbook |

## What Will Change Next Week?
- ICP:
- Message:
- Pricing:
- Delivery:
- Product:
- Trust:
"""
PY

cat > ops_runtime/decision_queue_builder.py <<'PY'
def build_decision_queue(bottlenecks):
    rows = []

    for idx, b in enumerate(bottlenecks, start=1):
        rows.append(
            f"| {idx} | {b['recommendation']} | Fix | {b['severity']} | {b['issue']} | {b['recommendation']} | Pending |"
        )

    if not rows:
        rows.append("| 1 | Continue weekly operating cadence | Continue | Low | No major bottleneck | Keep execution consistent | Pending |")

    return "# CEO Decision Queue\n\n| Priority | Decision | Type | Risk | Evidence | Recommendation | CEO Decision |\n|---:|---|---|---:|---|---|---|\n" + "\n".join(rows) + "\n"
PY

cat > ops_runtime/markdown_writer.py <<'PY'
from pathlib import Path


def write_markdown(path: str, content: str):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p
PY

cat > scripts/generate_ops_from_private.py <<'PY'
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ops_runtime.private_ops_reader import PrivateOpsReader
from ops_runtime.metrics_calculator import (
    calculate_pipeline_metrics,
    calculate_mrr_metrics,
    calculate_approval_metrics,
)
from ops_runtime.bottleneck_analyzer import analyze_bottlenecks
from ops_runtime.ceo_brief_generator import generate_ceo_brief
from ops_runtime.weekly_review_generator import generate_weekly_review
from ops_runtime.decision_queue_builder import build_decision_queue
from ops_runtime.markdown_writer import write_markdown


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True, help="Path to dealix-ops-private")
    args = parser.parse_args()

    private_root = Path(args.private_ops)

    reader = PrivateOpsReader(str(private_root))

    pipeline_rows = reader.read_csv("pipeline/pipeline_tracker.csv")
    mrr_rows = reader.read_csv("revenue/mrr_tracker.csv")
    approval_rows = reader.read_csv("trust/approval_log.csv")

    metrics = {}
    metrics.update(calculate_pipeline_metrics(pipeline_rows))
    metrics.update(calculate_mrr_metrics(mrr_rows))
    metrics.update(calculate_approval_metrics(approval_rows))

    bottlenecks = analyze_bottlenecks(metrics)

    daily_brief = generate_ceo_brief(metrics, bottlenecks)
    weekly_review = generate_weekly_review(metrics, bottlenecks)
    decision_queue = build_decision_queue(bottlenecks)

    write_markdown(str(private_root / "founder/daily_brief.md"), daily_brief)
    write_markdown(str(private_root / "learning/weekly_intelligence_review.md"), weekly_review)
    write_markdown(str(private_root / "founder/decision_queue.md"), decision_queue)

    print("PASS: generated private ops CEO brief, weekly review, and decision queue.")
    print(f"Lead count: {metrics.get('lead_count', 0)}")
    print(f"Contacted: {metrics.get('contacted', 0)}")
    print(f"Proposals: {metrics.get('proposal_sent', 0)}")
    print(f"Paid: {metrics.get('paid', 0)}")
    print(f"MRR: {metrics.get('mrr', 0)}")


if __name__ == "__main__":
    main()
PY

cat > scripts/verify_ops_runtime.py <<'PY'
from pathlib import Path

required = [
    "ops_runtime/private_ops_reader.py",
    "ops_runtime/metrics_calculator.py",
    "ops_runtime/ceo_brief_generator.py",
    "ops_runtime/weekly_review_generator.py",
    "ops_runtime/bottleneck_analyzer.py",
    "ops_runtime/decision_queue_builder.py",
    "scripts/generate_ops_from_private.py",
]

missing = [p for p in required if not Path(p).exists()]
empty = [p for p in required if Path(p).exists() and Path(p).stat().st_size == 0]

if missing or empty:
    if missing:
        print("Missing:")
        for p in missing:
            print("-", p)
    if empty:
        print("Empty:")
        for p in empty:
            print("-", p)
    raise SystemExit(1)

print("PASS: ops runtime exists.")
PY

python scripts/verify_ops_runtime.py
python -m compileall ops_runtime scripts

echo "== Dealix Master Operations Pack Complete =="

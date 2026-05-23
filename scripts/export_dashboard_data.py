import argparse
import json
import sys
from pathlib import Path
from datetime import date

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ops_runtime.private_ops_reader import PrivateOpsReader
from ops_runtime.metrics_calculator import (
    calculate_pipeline_metrics,
    calculate_mrr_metrics,
    calculate_approval_metrics,
)
from ops_runtime.bottleneck_analyzer import analyze_bottlenecks
from ops_runtime.alerts_generator import generate_alerts
from ops_runtime.target_scoring import calculate_target_score
from ops_runtime.founder_focus import choose_founder_focus


DEFAULT_WEEKLY_TARGETS = {
    "lead_count": 25,
    "contacted": 25,
    "replied": 5,
    "call_booked": 2,
    "proposal_sent": 1,
    "sample_sent": 3,
}

DEFAULT_MONTHLY_TARGETS = {
    "paid": 1,
    "delivered": 1,
    "retainer": 1,
}


def company_status(metrics, alerts):
    if any(a["level"] == "red" for a in alerts):
        return "FIX"
    if metrics.get("paid", 0) > 0 or metrics.get("retainer", 0) > 0:
        return "PASS"
    return "READY INTERNAL"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    parser.add_argument("--out", default="dashboard_data/company_metrics.json")
    args = parser.parse_args()

    reader = PrivateOpsReader(args.private_ops)

    metrics = {}
    metrics.update(calculate_pipeline_metrics(reader.read_csv("pipeline/pipeline_tracker.csv")))
    metrics.update(calculate_mrr_metrics(reader.read_csv("revenue/mrr_tracker.csv")))
    metrics.update(calculate_approval_metrics(reader.read_csv("trust/approval_log.csv")))

    bottlenecks = analyze_bottlenecks(metrics)
    alerts = generate_alerts(metrics, bottlenecks)

    weekly_score = calculate_target_score(metrics, DEFAULT_WEEKLY_TARGETS)
    monthly_score = calculate_target_score(metrics, DEFAULT_MONTHLY_TARGETS)

    payload = {
        "summary": {
            "date": date.today().isoformat(),
            "company_status": company_status(metrics, alerts),
            "founder_focus": choose_founder_focus(metrics, bottlenecks)
        },
        "metrics": metrics,
        "targets": {
            "weekly": DEFAULT_WEEKLY_TARGETS,
            "monthly": DEFAULT_MONTHLY_TARGETS
        },
        "target_status": {
            "weekly_score": weekly_score,
            "monthly_score": monthly_score
        },
        "alerts": alerts,
        "bottlenecks": bottlenecks,
        "decisions": [
            {
                "priority": idx + 1,
                "decision": b["recommendation"],
                "type": "Fix",
                "risk": b["severity"],
                "recommendation": b["recommendation"]
            }
            for idx, b in enumerate(bottlenecks)
        ]
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"PASS: wrote dashboard data to {out}")


if __name__ == "__main__":
    main()

import argparse
import json
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

    payload = {
        "metrics": metrics,
        "bottlenecks": bottlenecks,
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"PASS: wrote dashboard data to {out}")


if __name__ == "__main__":
    main()

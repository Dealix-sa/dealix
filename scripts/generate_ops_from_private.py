import argparse
from pathlib import Path

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
from ops_runtime.scorecard_updater import build_scorecard
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
    scorecard = build_scorecard(metrics, bottlenecks)

    write_markdown(str(private_root / "founder/daily_brief.md"), daily_brief)
    write_markdown(str(private_root / "learning/weekly_intelligence_review.md"), weekly_review)
    write_markdown(str(private_root / "founder/decision_queue.md"), decision_queue)
    write_markdown(str(private_root / "founder/company_os_scorecard.md"), scorecard)

    print("PASS: generated private ops CEO brief, weekly review, scorecard, and decision queue.")
    print(f"Lead count: {metrics.get('lead_count', 0)}")
    print(f"Contacted: {metrics.get('contacted', 0)}")
    print(f"Proposals: {metrics.get('proposal_sent', 0)}")
    print(f"Paid: {metrics.get('paid', 0)}")
    print(f"MRR: {metrics.get('mrr', 0)}")


if __name__ == "__main__":
    main()

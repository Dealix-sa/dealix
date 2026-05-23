import argparse
from pathlib import Path

from ops_runtime.private_ops_reader import PrivateOpsReader
from ops_runtime.metrics_calculator import (
    calculate_pipeline_metrics,
    calculate_mrr_metrics,
    calculate_approval_metrics,
)
from ops_runtime.bottleneck_analyzer import analyze_bottlenecks
from ops_runtime.weekly_metrics_writer import append_weekly_metrics
from ops_runtime.weekly_comparison import compare_latest_weeks
from ops_runtime.learning_decision_engine import recommend_learning_decision
from ops_runtime.weekly_review_v2_generator import generate_weekly_review_v2
from ops_runtime.markdown_writer import write_markdown


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()

    private_ops = Path(args.private_ops).resolve()
    reader = PrivateOpsReader(str(private_ops))

    metrics = {}
    metrics.update(calculate_pipeline_metrics(reader.read_csv("pipeline/pipeline_tracker.csv")))
    metrics.update(calculate_mrr_metrics(reader.read_csv("revenue/mrr_tracker.csv")))
    metrics.update(calculate_approval_metrics(reader.read_csv("trust/approval_log.csv")))

    bottlenecks = analyze_bottlenecks(metrics)

    history_path = append_weekly_metrics(str(private_ops), metrics)
    history_rows = reader.read_csv("metrics_history/weekly_metrics.csv")
    comparison = compare_latest_weeks(history_rows)

    learning_decision = recommend_learning_decision(metrics, bottlenecks, comparison)
    review = generate_weekly_review_v2(metrics, bottlenecks, comparison, learning_decision)

    week_file = private_ops / f"weekly_reviews/{metrics.get('week_ending', '')}.md"
    if "week_ending" not in metrics:
        from datetime import date
        week_file = private_ops / f"weekly_reviews/{date.today().isoformat()}.md"

    write_markdown(str(private_ops / "founder/weekly_ceo_review.md"), review)
    write_markdown(str(private_ops / "learning/weekly_intelligence_review.md"), review)
    write_markdown(str(week_file), review)

    print("PASS: weekly automation completed.")
    print(f"Updated: {history_path}")
    print(f"Updated: {private_ops / 'founder/weekly_ceo_review.md'}")
    print(f"Updated: {private_ops / 'learning/weekly_intelligence_review.md'}")
    print(f"Recommended playbook update: {learning_decision['recommended_file']}")
    print(f"Update note: {learning_decision['update']}")


if __name__ == "__main__":
    main()

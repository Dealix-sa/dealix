from pathlib import Path
import csv

required = [
    "sprint/current_sprint.md",
    "sprint/daily_execution_log.md",
    "sprint/sprint_scorecard.csv",
    "pipeline/pipeline_tracker.csv",
    "founder/daily_brief.md",
    "founder/decision_queue.md",
    "learning/weekly_intelligence_review.md",
]

failures = []

for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size == 0:
        failures.append(f"Empty: {file}")

scorecard = Path("sprint/sprint_scorecard.csv")
if scorecard.exists():
    with scorecard.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        for header in ["day", "focus", "target", "actual", "status", "evidence", "next_action"]:
            if header not in headers:
                failures.append(f"sprint_scorecard missing header: {header}")

if failures:
    print("Priority sprint private verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

print("PASS: private priority sprint is ready.")

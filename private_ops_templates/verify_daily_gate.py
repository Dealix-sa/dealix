from pathlib import Path
import csv

failures = []

required = [
    "sprint/daily_gate.md",
    "sprint/daily_execution_log.md",
    "pipeline/pipeline_tracker.csv",
    "founder/approvals_waiting.md",
]

for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size == 0:
        failures.append(f"Empty: {file}")

pipeline = Path("pipeline/pipeline_tracker.csv")
if pipeline.exists():
    with pipeline.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for i, row in enumerate(rows, start=2):
        if not (row.get("stage") or "").strip():
            failures.append(f"pipeline row {i} missing stage")
        if not (row.get("next_action") or "").strip():
            failures.append(f"pipeline row {i} missing next_action")

if failures:
    print("Daily gate verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

print("PASS: daily execution gate passed.")

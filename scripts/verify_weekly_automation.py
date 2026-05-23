from pathlib import Path

required = [
    "ops_runtime/weekly_metrics_writer.py",
    "ops_runtime/weekly_comparison.py",
    "ops_runtime/learning_decision_engine.py",
    "ops_runtime/weekly_review_v2_generator.py",
    "scripts/run_weekly_automation.py",
]

failures = []

for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size == 0:
        failures.append(f"Empty: {file}")

if failures:
    print("Weekly automation verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

print("PASS: weekly automation files exist.")

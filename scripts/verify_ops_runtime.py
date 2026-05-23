from pathlib import Path

required = [
    "ops_runtime/private_ops_reader.py",
    "ops_runtime/metrics_calculator.py",
    "ops_runtime/ceo_brief_generator.py",
    "ops_runtime/weekly_review_generator.py",
    "ops_runtime/bottleneck_analyzer.py",
    "ops_runtime/decision_queue_builder.py",
    "ops_runtime/scorecard_updater.py",
    "ops_runtime/markdown_writer.py",
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

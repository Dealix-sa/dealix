from pathlib import Path

required = [
    "execution_engine/evidence_scanner.py",
    "execution_engine/stage_checklist_updater.py",
    "execution_engine/evidence_report_generator.py",
]

failures = []

for file in required:
    p = Path(file)
    if not p.exists():
        failures.append(f"Missing: {file}")
    elif p.stat().st_size == 0:
        failures.append(f"Empty: {file}")

if failures:
    print("Stage evidence automation failed:")
    for f in failures:
        print("-", f)
    raise SystemExit(1)

print("PASS: stage evidence automation is ready.")

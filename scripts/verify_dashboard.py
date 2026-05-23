"""CEO Dashboard v1 verifier.

Confirms the v1 ops_runtime modules and demo data exist so the v2 export
pipeline has the inputs it depends on.
"""
from pathlib import Path

required = [
    "ops_runtime/private_ops_reader.py",
    "ops_runtime/metrics_calculator.py",
    "ops_runtime/bottleneck_analyzer.py",
    "scripts/export_dashboard_data.py",
]

failures = []

for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size == 0:
        failures.append(f"Empty: {file}")

if failures:
    print("Dashboard v1 verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

print("PASS: CEO dashboard v1 prerequisites are valid.")

"""Verify that the Dealix Implementation Automation Pack is complete.

Each required file must exist and contain at least 100 bytes of content so
empty stubs do not satisfy the gate. Run from the repo root; exits non-zero
on any failure so it can wire into CI as a status check.
"""

from pathlib import Path

required = [
    "scripts/bootstrap_dealix_os.py",
    "scripts/bootstrap_private_ops.py",
    "scripts/implementation_sprint_status.py",
    "scripts/verify_market_execution_evidence.py",
    "scripts/generate_stoplight_report.py",
    "docs/ops/NO_MORE_SYSTEMS_GATE.md",
]

failures = []
for file in required:
    p = Path(file)
    if not p.exists():
        failures.append(f"Missing: {file}")
    elif p.stat().st_size < 100:
        failures.append(f"Too short: {file}")

if failures:
    print("Implementation automation pack verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)

print("PASS: implementation automation pack is ready.")

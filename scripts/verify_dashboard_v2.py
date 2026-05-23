"""Verify the dashboard v2 surface exists at minimum."""

from pathlib import Path

candidates = [
    "DASHBOARD.md",
    "dashboard",
    "docs/19_command_os",
]

found_any = False
failures = []

for entry in candidates:
    path = Path(entry)
    if path.exists():
        found_any = True
        if path.is_file() and path.stat().st_size < 50:
            failures.append(f"Too short: {entry}")

if not found_any:
    failures.append("No dashboard surface found (expected DASHBOARD.md or dashboard/ or docs/19_command_os).")

if failures:
    print("Dashboard v2 verification failed:")
    for f in failures:
        print("-", f)
    raise SystemExit(1)

print("PASS: dashboard surface is present.")

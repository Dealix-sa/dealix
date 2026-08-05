"""Dealix priority full ops verifier.

Runs revenue/trust/delivery first, then the supporting checks. Any failure
fails the whole pipeline.
"""

import subprocess
import sys
from pathlib import Path

CHECKS = [
    "scripts/verify_revenue_control.py",
    "scripts/verify_trust_control.py",
    "scripts/verify_delivery_control.py",
    "scripts/verify_company_os_deep.py",
    "scripts/verify_dashboard_v2.py",
    "scripts/verify_cli.py",
    "scripts/verify_weekly_automation.py",
]

failed = []

for script in CHECKS:
    if not Path(script).exists():
        failed.append(f"Missing check: {script}")
        continue

    print(f"\n== Running: python {script} ==")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        failed.append(script)

if failed:
    print("\nFAILED CHECKS:")
    for item in failed:
        print("-", item)
    sys.exit(1)

print("\nPASS: Dealix priority full ops verification passed.")

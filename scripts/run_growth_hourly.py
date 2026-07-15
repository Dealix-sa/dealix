"""Dealix 24/7 Growth Factory - hourly runner.

Runs safe internal tasks only. No external sending.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


SAFE_INTERNAL_TASKS = [
    ["scripts/create_research_queue.py"],
    ["scripts/generate_acquisition_daily_report.py"],
    ["scripts/generate_stoplight_report.py"],
]


def run(cmd: list[str]) -> int:
    print("+", " ".join(cmd))
    result = subprocess.run(cmd, check=False)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()

    root = Path(args.private_ops).resolve()
    root.mkdir(parents=True, exist_ok=True)

    failures = 0
    for task in SAFE_INTERNAL_TASKS:
        script_path = Path(task[0])
        if not script_path.exists():
            print(f"skip (missing): {script_path}")
            continue
        rc = run([sys.executable, *task, "--private-ops", str(root)])
        if rc != 0:
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

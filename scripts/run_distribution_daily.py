"""Daily distribution orchestrator.

Runs the sequence of growth and reporting jobs in order against the private
ops directory. Failures are logged but do not halt the chain.
"""

import argparse
import subprocess
import sys
from pathlib import Path

COMMANDS = [
    ["scripts/run_growth_hourly.py"],
    ["scripts/run_growth_4h.py"],
    ["scripts/generate_distribution_command_center.py"],
    ["scripts/generate_acquisition_daily_report.py"],
    ["scripts/generate_stoplight_report.py"],
]


def run(cmd, private_ops):
    full = [sys.executable] + cmd + ["--private-ops", str(private_ops)]
    print("+", " ".join(full))
    subprocess.run(full, check=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()
    private_ops = Path(args.private_ops).resolve()
    for cmd in COMMANDS:
        run(cmd, private_ops)


if __name__ == "__main__":
    main()

"""Render execution assurance report for the CEO."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

# Allow running directly from repo root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ops_runtime.execution_assurance import calculate_execution_assurance  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()

    root = Path(args.private_ops).resolve()
    result = calculate_execution_assurance(str(root))

    check_rows = "\n".join(
        f"| {name} | {'PASS' if passed else 'MISSING'} |"
        for name, passed in result["checks"].items()
    )
    missing = "\n".join(f"- {item}" for item in result["missing"]) or "- None"

    content = f"""# Execution Assurance Report

## Date
{date.today().isoformat()}

## Score
{result['score']} / 100

## Status
{result['status']}

## Evidence Count
{result['evidence_count']}

## Checks
| Check | Status |
|---|---|
{check_rows}

## Missing Evidence
{missing}

## CEO Interpretation
- SETUP: complete operating files and first evidence.
- PARTIAL: execute missing market actions.
- EXECUTING: push toward proposal/payment/delivery.
- OPERATING: maintain cadence and improve systems.

## CEO Rule
Do not add new systems until missing evidence is resolved.
"""

    out = root / "evidence/execution_assurance_report.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")

    print("PASS: execution assurance report generated.")
    print(f"Score: {result['score']} / 100")
    print(f"Status: {result['status']}")
    print(f"Written: {out}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Run one governed day — the single canonical Full Ops entrypoint (M3).

Replaces the 6+ subprocess-chain run_* scripts with one observable call.
Every phase outcome is recorded to the durable governance log (M4).

Usage:
    python scripts/dealix_governed_day.py            # run the day
    python scripts/dealix_governed_day.py --dry-run  # record phases, no side effects
    python scripts/dealix_governed_day.py --json     # machine-readable output
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.orchestrator.governed_day import run_governed_day  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dealix governed day runner")
    parser.add_argument("--dry-run", action="store_true", help="record phases without executing")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args(argv)

    result = run_governed_day(dry_run=args.dry_run)

    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"Governed day {result.correlation_id} — verdict: {result.verdict.upper()}")
        for phase in result.phases:
            mark = {"ok": "[OK]", "degraded": "[!!]", "blocked": "[XX]"}.get(phase.status, "[??]")
            line = f"  {mark} {phase.name}: {phase.summary or phase.error}"
            print(line)
        c = result.counts
        print(f"  phases={c.get('phases', 0)} ok={c.get('ok', 0)} "
              f"degraded={c.get('degraded', 0)} blocked={c.get('blocked', 0)}")

    print(f"DEALIX_GOVERNED_DAY_VERDICT={result.verdict.upper()}")
    return 0 if result.verdict != "blocked" else 1


if __name__ == "__main__":
    sys.exit(main())

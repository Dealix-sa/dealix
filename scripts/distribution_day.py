#!/usr/bin/env python3
"""Distribution Day (Revenue Execution OS) — the one daily command.

Runs the full governed pipeline in-process:
  prospects → drafts → quality gate → queue → follow-ups → proposals
           → proof packs → payment handoff → renewals → metrics → win/loss
then writes reports/distribution/DISTRIBUTION_DAY.md and prints the verdict.
Nothing is sent — the output is the founder's prioritized to-do.

Prints ``DEALIX_DISTRIBUTION_DAY=PASS|FAIL`` (parity with other Dealix verifiers).
Exit code 1 on FAIL.

Usage:
    python scripts/distribution_day.py
    python scripts/distribution_day.py --today 2026-06-02 --json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402
from dealix.distribution.day import run_day  # noqa: E402
from dealix.distribution.paths import REPORTS_DIR  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description="Run the full distribution day pipeline.")
    p.add_argument("--prospects", type=Path, default=None)
    p.add_argument("--today", type=date.fromisoformat, default=None, help="YYYY-MM-DD")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    result = run_day(args.prospects, today=args.today, write_report=True)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        k = result["metrics"]["kpis"]
        print("DISTRIBUTION_DAY:")
        print(f"  pending drafts : {k['pending_drafts']}")
        print(f"  due follow-ups : {k['due_followups']}")
        print(f"  proposal drafts: {k['proposal_drafts']}")
        print(f"  proof packs    : {k['proof_packs']}")
        print(f"  report         : {REPORTS_DIR / 'DISTRIBUTION_DAY.md'}")
        print(f"  next action    : {result['founder_action_ar']}")

    print(f"DEALIX_DISTRIBUTION_DAY={result['verdict']}")
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"DISTRIBUTION_DAY: FAIL — {exc}", file=sys.stderr)
        print("DEALIX_DISTRIBUTION_DAY=FAIL")
        raise SystemExit(1) from exc

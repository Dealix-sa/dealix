#!/usr/bin/env python3
"""Run Dealix Full Company OS in safe draft-only mode."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.full_company_os import RunConfig, run_daily_cycle  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Dealix Full Company OS daily command loop.")
    parser.add_argument("--client", default="dealix")
    parser.add_argument("--mode", default="draft-only", choices=["draft-only"])
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--autonomy-level", type=int, default=3, choices=[0, 1, 2, 3, 4])
    parser.add_argument("--output-root", default="reports/full_company_os")
    parser.add_argument("--json", action="store_true", help="Print JSON summary instead of human text.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_daily_cycle(
        RunConfig(
            client=args.client,
            mode=args.mode,
            limit=args.limit,
            autonomy_level=args.autonomy_level,
            output_root=args.output_root,
        )
    )
    summary = {
        "status": "PASS",
        "mode": args.mode,
        "client": args.client,
        "opportunities": len(result.opportunities),
        "drafts": len(result.drafts),
        "approvals": len(result.approvals),
        "proof_events": len(result.proof_log),
        "improvements": len(result.improvements),
        "output_files": result.output_files,
    }
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(
            "FULL_COMPANY_OS=PASS "
            f"client={summary['client']} mode={summary['mode']} "
            f"opportunities={summary['opportunities']} drafts={summary['drafts']} "
            f"approvals={summary['approvals']} proof={summary['proof_events']} "
            f"report={summary['output_files']['latest_report']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

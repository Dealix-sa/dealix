#!/usr/bin/env python3
"""Generate the daily command report (and optionally the weekly proof pack).

Reads the current opportunity graph store and renders markdown. Does not
re-score — run run_daily_opportunity_targeting.py first for a fresh cycle.

Usage:
    python scripts/commercial/generate_daily_command_report.py
    python scripts/commercial/generate_daily_command_report.py --weekly-proof-pack
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.opportunity_graph.reports import write_daily_report, write_weekly_proof_pack
from dealix.opportunity_graph.store import get_store


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render daily command report / weekly proof pack.")
    parser.add_argument("--weekly-proof-pack", action="store_true", help="Also write the weekly proof pack.")
    parser.add_argument("--client-id", default="dealix_internal", help="Client id for the proof pack.")
    args = parser.parse_args(argv)

    store = get_store()
    daily_path = write_daily_report(store=store)
    print(f"Daily command report: {daily_path}")

    if args.weekly_proof_pack:
        proof_path = write_weekly_proof_pack(store=store, client_id=args.client_id)
        print(f"Weekly proof pack: {proof_path}")

    print("Draft-only. No external sends.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

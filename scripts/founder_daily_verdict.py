#!/usr/bin/env python3
"""Founder daily verdict — one GO/WARN/BLOCKED signal each morning."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.founder_daily_verdict import build_founder_daily_verdict  # noqa: E402
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--api-base",
        default=os.getenv("DEALIX_API_BASE", "https://api.dealix.me"),
        help="Live API base for trust probes (used when --with-live is set).",
    )
    p.add_argument(
        "--with-live",
        action="store_true",
        help="Probe live API trust layer (default: offline repo-only verification).",
    )
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    blob = build_founder_daily_verdict(
        api_base=args.api_base if args.with_live else None,
        skip_live=not args.with_live,
    )

    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print(f"== Founder daily verdict · {blob['iso_date']} ==")
        print(f"  verdict: {blob['verdict']}")
        prod = blob["production_gates"]
        print(f"  production_gates: {prod['verdict']} (api={prod['api_base'] or 'offline'})")
        kpi = blob["kpi_freshness"]
        print(
            f"  kpi: {kpi['status']} (pending={kpi['pending_count']} ready={kpi['ready_count']})"
        )
        morning = blob["morning_ops"]
        print(
            f"  morning: {morning['status']} "
            f"(today_present={morning['today_present']} latest={morning.get('latest_path')})"
        )
        for action in blob.get("founder_actions_ar") or []:
            print(f"  ACTION: {action}")
        print()
        print("  commands:")
        for label, cmd in blob["commands"].items():
            print(f"    {label}: {cmd}")

    print(f"FOUNDER_DAILY_VERDICT={blob['verdict']}")
    return 0 if blob["verdict"] in ("GO", "WARN") else 1


if __name__ == "__main__":
    raise SystemExit(main())

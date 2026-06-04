#!/usr/bin/env python3
"""Dealix Daily Draft Factory — generate >=400 review-only drafts.

400 drafts != 400 sends. These are review-only drafts written to the daily
output folder for founder review. NOTHING is sent externally.

Usage:
    python scripts/commercial_generate_400_drafts.py --target 400
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import commercial_launch_core as core  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate >=400 review-only drafts.")
    parser.add_argument("--target", type=int, default=400, help="Minimum primary drafts (default 400)")
    parser.add_argument("--date", default=None, help="Override date (YYYY-MM-DD)")
    parser.add_argument("--leads", default=None, help="Path to seed leads JSONL")
    args = parser.parse_args(argv)

    configs = core.load_all_configs()
    leads = core.load_seed_leads(args.leads) if args.leads else core.load_seed_leads()
    date_str = args.date or core.today_str()

    drafts = core.generate_drafts(target=args.target, leads=leads, configs=configs, date_str=date_str)
    out = core.write_outputs(drafts, configs, date_str)

    # also run the safety audit so every output folder carries a safety report
    try:
        import commercial_safety_audit as audit
        audit.run_audit(date_str=date_str, out_dir=out)
    except Exception as exc:  # pragma: no cover - defensive
        print(f"WARN: safety audit step skipped: {exc}", file=sys.stderr)

    m = core.compute_metrics(drafts)
    print(f"Generated {m['drafts_generated']} drafts (target {args.target}).")
    print(f"  Founder review queue: {m['founder_review_count']}")
    print(f"  ready_for_manual_copy={m['ready_for_manual_copy']} "
          f"founder_review={m['founder_review']} needs_research={m['needs_research']}")
    print(f"  rejected_quality={m['rejected_quality']} rejected_compliance={m['rejected_compliance']}")
    print(f"  all_send_disallowed={m['all_send_disallowed']} all_send_blocked={m['all_send_blocked']}")
    print(f"Outputs: {out}")

    if m["drafts_generated"] < args.target:
        print("ERROR: fewer than target drafts generated.", file=sys.stderr)
        return 1
    if not (m["all_send_disallowed"] and m["all_send_blocked"]):
        print("ERROR: safety flags violated.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

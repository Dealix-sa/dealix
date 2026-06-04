#!/usr/bin/env python3
"""Generate 400+ founder-review drafts for the day and write all outputs.

The system NEVER sends. Every draft is approval-gated. Usage:

    python scripts/commercial_generate_400_drafts.py --target 400
"""

from __future__ import annotations

import argparse
import sys

import commercial_launch_lib as lib


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dealix 400+ daily draft factory")
    parser.add_argument("--target", type=int, default=400, help="Minimum number of drafts to generate")
    parser.add_argument("--date", type=str, default=None, help="Override output date (YYYY-MM-DD)")
    args = parser.parse_args(argv)

    config = lib.load_all_config()
    drafts = lib.generate_drafts(target=args.target, config=config)

    # Hard safety guarantee before anything is written.
    lib.assert_safety(drafts)

    if len(drafts) < args.target:
        print(f"FAIL: generated {len(drafts)} < target {args.target}", file=sys.stderr)
        return 1

    out = lib.write_outputs(drafts, config, date=args.date)
    summary = lib.summarize(drafts)

    print(f"✅ Generated {summary['drafts_generated']} drafts (target {args.target})")
    print(f"   Founder review: {summary['founder_review_count']}")
    print(f"   Rejected quality: {summary['rejected_quality']}")
    print(f"   Rejected compliance: {summary['rejected_compliance']}")
    print(f"   Needs research: {summary['needs_research']}")
    print(f"   Outputs: {out}")
    print("   Safety: send_allowed=false, external_send_blocked=true, no_auto_send=true on every draft.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

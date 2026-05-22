#!/usr/bin/env python3
"""Founder Health Brief — one number, sub-scores, and the next 5 actions.

Single command, single output. Composes:
  - Evidence flow (rolling 7 days, real events only)
  - First-paid Diagnostic tracker (Article 13)
  - PDPL operational compliance pass
  - Strongest-plan wiring status (138 tasks)
  - Lead inbox freshness (waiting > N hours)

Hard rules:
  - Article 4: NEVER auto-sends. Prints to stdout or writes to file.
  - Article 8: counts are operational estimates (is_estimate=True).
  - Article 11: compose-only — no new business logic.

Usage:
    # Print Arabic+English brief to terminal (default):
    python3 scripts/founder_health_brief.py

    # JSON output (machine-readable, for /api/v1/founder/health-score):
    python3 scripts/founder_health_brief.py --format json

    # Write markdown to gitignored briefs folder:
    python3 scripts/founder_health_brief.py --out data/founder_briefs/health_today.md

    # Customize inbox staleness threshold:
    python3 scripts/founder_health_brief.py --stale-hours 12
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from dealix.commercial_ops.founder_health_score import (  # noqa: E402
    compute_founder_health_score,
    render_health_brief_markdown,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--format",
        choices=("md", "json"),
        default="md",
        help="Output format (default: md)",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Write to this path instead of stdout",
    )
    parser.add_argument(
        "--stale-hours",
        type=int,
        default=24,
        help="Lead-inbox staleness threshold in hours (default: 24)",
    )
    parser.add_argument(
        "--exit-code-by-verdict",
        action="store_true",
        help="Exit 0 on HEALTHY, 1 on CAUTION, 2 on ACTION_NEEDED (for CI gates)",
    )
    args = parser.parse_args()

    ensure_stdout_utf8()

    snap = compute_founder_health_score(stale_hours=max(1, min(args.stale_hours, 168)))

    if args.format == "json":
        body = json.dumps(snap, ensure_ascii=False, indent=2)
    else:
        body = render_health_brief_markdown(snap)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(body, encoding="utf-8")
        print(f"wrote {out_path}")
    else:
        print(body)

    if args.exit_code_by_verdict:
        verdict = snap.get("verdict")
        if verdict == "HEALTHY":
            return 0
        if verdict == "CAUTION":
            return 1
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

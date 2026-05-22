#!/usr/bin/env python3
"""Founder Action Inbox CLI — prioritized list across subsystems.

Produces a single P0→P3 list of items needing founder attention:
  - Pending approvals (high/med/low risk)
  - Stale leads in the inbox (waiting > N hours)
  - Evidence gap (no events today / weak week)
  - PDPL pass open items
  - First-paid Diagnostic state (Article 13)
  - Strongest-plan wiring gaps

Hard rules:
  - Article 4: read-only, never auto-sends. Prints/writes only.
  - Article 8: counts are operational estimates.
  - Article 11: compose-only — aggregates existing modules.

Usage:
    # Print Arabic+English markdown (default):
    python3 scripts/founder_action_inbox.py

    # JSON output:
    python3 scripts/founder_action_inbox.py --format json

    # Write to file:
    python3 scripts/founder_action_inbox.py --out data/founder_briefs/inbox_today.md

    # Customize threshold:
    python3 scripts/founder_action_inbox.py --stale-hours 12 --limit 20
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from dealix.commercial_ops.founder_action_inbox import (  # noqa: E402
    build_action_inbox,
    render_inbox_markdown,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--format", choices=("md", "json"), default="md")
    parser.add_argument("--out", type=str, default=None)
    parser.add_argument("--stale-hours", type=int, default=24)
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument(
        "--exit-code-by-verdict",
        action="store_true",
        help="Exit 2 on BLOCKED, 1 on ACTIVE_DAY, 0 on MAINTENANCE/CLEAR",
    )
    args = parser.parse_args()

    ensure_stdout_utf8()

    snap = build_action_inbox(
        stale_hours=max(1, min(args.stale_hours, 168)),
        limit=max(1, min(args.limit, 200)),
    )

    if args.format == "json":
        body = json.dumps(snap, ensure_ascii=False, indent=2, default=str)
    else:
        body = render_inbox_markdown(snap)

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(body, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(body)

    if args.exit_code_by_verdict:
        v = snap.get("verdict")
        if v == "BLOCKED":
            return 2
        if v == "ACTIVE_DAY":
            return 1
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())

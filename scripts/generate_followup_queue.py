#!/usr/bin/env python3
"""Follow-up Queue (Revenue Execution OS) — who to re-contact today (no send).

Computes due follow-ups from prospects' last-contact dates and appends them to
data/followups/followups.jsonl. Reminders only — the founder sends manually.

Usage:
    python scripts/generate_followup_queue.py
    python scripts/generate_followup_queue.py --today 2026-06-02
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
from dealix.distribution import followups  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description="Generate the follow-up queue (reminders only).")
    p.add_argument("--prospects", type=Path, default=None)
    p.add_argument("--today", type=date.fromisoformat, default=None, help="YYYY-MM-DD")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    summary = followups.run_generation(args.prospects, today=args.today)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        bp = summary["by_priority"]
        print("FOLLOWUP_QUEUE:")
        print(f"  due total      : {summary['due_total']}")
        print(f"  new followups  : {summary['new_followups']}")
        print(f"  by priority    : high={bp['high']} medium={bp['medium']} low={bp['low']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FOLLOWUP_QUEUE: FAIL — {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

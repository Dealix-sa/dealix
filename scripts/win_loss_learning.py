#!/usr/bin/env python3
"""Win/Loss Learning (Revenue Execution OS) — every outcome teaches the system.

Aggregates recorded outcomes into a learning summary + next changes, and writes
reports/distribution/WIN_LOSS_LEARNING.md. ``--record`` appends one outcome.

Usage:
    python scripts/win_loss_learning.py
    python scripts/win_loss_learning.py --record --company "Acme" --outcome lost \\
        --reason price --sector clinics --lesson "start with diagnostic"
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402
from dealix.distribution import win_loss  # noqa: E402
from dealix.distribution.paths import REPORTS_DIR  # noqa: E402
from dealix.distribution.reports import render_win_loss  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description="Win/loss learning loop.")
    p.add_argument("--record", action="store_true", help="Append one outcome.")
    p.add_argument("--company", default="")
    p.add_argument("--outcome", choices=sorted(win_loss.VALID_OUTCOMES), default="lost")
    p.add_argument("--reason", default="")
    p.add_argument("--sector", default="")
    p.add_argument("--objection", default="")
    p.add_argument("--offer", default="")
    p.add_argument("--channel", default="")
    p.add_argument("--lesson", default="")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    if args.record:
        if not args.company or not args.reason:
            print("WIN_LOSS: --record requires --company and --reason", file=sys.stderr)
            return 1
        rec = win_loss.record_outcome(
            company=args.company,
            outcome=args.outcome,
            reason=args.reason,
            sector=args.sector,
            objection=args.objection,
            offer=args.offer,
            channel=args.channel,
            lesson=args.lesson,
        )
        print(f"WIN_LOSS recorded: {rec['id']} ({rec['outcome']})")

    summary = win_loss.learning_summary()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "WIN_LOSS_LEARNING.md").write_text(render_win_loss(summary), encoding="utf-8")

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print("WIN_LOSS_LEARNING:")
        print(f"  total      : {summary['total']}")
        print(f"  by outcome : {summary['by_outcome']}")
        print(f"  win rate   : {summary['win_rate_pct']}%")
        print("  next changes:")
        for c in summary["next_changes"]:
            print(f"    - {c}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"WIN_LOSS_LEARNING: FAIL — {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

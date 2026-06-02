#!/usr/bin/env python3
"""Weekly Distribution Review (Revenue Execution OS) — the Sunday board view.

Composes the funnel + win/loss into a weekly review with founder decision
prompts, and writes reports/distribution/WEEKLY_DISTRIBUTION_REVIEW.md.

Usage:
    python scripts/distribution_weekly_review.py
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
from dealix.distribution import metrics  # noqa: E402
from dealix.distribution.paths import REPORTS_DIR  # noqa: E402
from dealix.distribution.reports import render_weekly  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description="Weekly distribution review.")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    snapshot = metrics.compute_metrics()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORTS_DIR / "WEEKLY_DISTRIBUTION_REVIEW.md"
    out.write_text(render_weekly(snapshot), encoding="utf-8")

    if args.json:
        print(json.dumps(snapshot, ensure_ascii=False, indent=2))
    else:
        k = snapshot["kpis"]
        print("WEEKLY_DISTRIBUTION_REVIEW:")
        print(f"  won/lost     : {k['won_deals']}/{k['lost_deals']}")
        print(f"  due followups: {k['due_followups']}")
        print(f"  report       : {out}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"WEEKLY_DISTRIBUTION_REVIEW: FAIL — {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

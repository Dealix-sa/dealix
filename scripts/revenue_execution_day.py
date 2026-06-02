#!/usr/bin/env python3
"""Revenue Execution OS — daily distribution report generator.

Read-only: composes Markdown reports from the JSONL stores. Never sends,
charges, or mutates customer-facing state.

    python3 scripts/revenue_execution_day.py [--output DIR] [--print]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from auto_client_acquisition.revenue_execution_os.daily_report import (
    render_daily_report,
    render_followup_queue_report,
    render_metrics_report,
    render_win_loss_report,
)


def _write(out_dir: Path, name: str, content: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / name
    path.write_text(content, encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Generate the daily distribution reports")
    ap.add_argument("--output", default="reports/distribution", help="output directory")
    ap.add_argument(
        "--print", action="store_true", dest="do_print", help="also print the daily report"
    )
    args = ap.parse_args(argv)

    out = Path(args.output)
    written = [
        _write(out, "DISTRIBUTION_DAY.md", render_daily_report()),
        _write(out, "FOLLOWUP_QUEUE.md", render_followup_queue_report()),
        _write(out, "DISTRIBUTION_METRICS.md", render_metrics_report()),
        _write(out, "WIN_LOSS_LEARNING.md", render_win_loss_report()),
    ]
    for p in written:
        print(f"wrote {p}")
    if args.do_print:
        print()
        print(render_daily_report())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

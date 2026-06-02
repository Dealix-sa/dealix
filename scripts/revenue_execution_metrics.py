#!/usr/bin/env python3
"""Revenue Execution OS — distribution metrics.

Prints daily + weekly metrics and writes reports/distribution/DISTRIBUTION_METRICS.md.
Read-only: counts over recorded entities only; no invented numbers.

    python3 scripts/revenue_execution_metrics.py [--output DIR] [--json]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from auto_client_acquisition.revenue_execution_os.daily_report import (
    render_metrics_report,
)
from auto_client_acquisition.revenue_execution_os.metrics import (
    daily_metrics,
    weekly_metrics,
)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Distribution metrics")
    ap.add_argument("--output", default="reports/distribution", help="output directory")
    ap.add_argument("--json", action="store_true", help="print metrics as JSON")
    args = ap.parse_args(argv)

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "DISTRIBUTION_METRICS.md"
    path.write_text(render_metrics_report(), encoding="utf-8")
    print(f"wrote {path}")

    payload = {"daily": daily_metrics(), "weekly": weekly_metrics()}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for scope, data in payload.items():
            print(f"\n[{scope}]")
            for k, v in data.items():
                print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

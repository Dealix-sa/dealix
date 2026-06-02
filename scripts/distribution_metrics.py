#!/usr/bin/env python3
"""Distribution Metrics (Revenue Execution OS) — funnel cockpit across ledgers.

Aggregates drafts → follow-ups → proposals → proof packs → payments → renewals
plus win/loss, prints KPIs, and writes reports/distribution/DISTRIBUTION_METRICS.md.

Usage:
    python scripts/distribution_metrics.py
    python scripts/distribution_metrics.py --json
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
from dealix.distribution.reports import render_metrics  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description="Distribution funnel metrics.")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    snapshot = metrics.compute_metrics()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "DISTRIBUTION_METRICS.md").write_text(render_metrics(snapshot), encoding="utf-8")

    if args.json:
        print(json.dumps(snapshot, ensure_ascii=False, indent=2))
    else:
        k = snapshot["kpis"]
        f = snapshot["funnel"]
        print("DISTRIBUTION_METRICS:")
        for key, val in k.items():
            print(f"  {key:18}: {val}")
        print(
            f"  funnel: drafts={f['drafts']} approved={f['approved_drafts']} "
            f"proposals={f['proposals']} paid={f['paid']}"
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"DISTRIBUTION_METRICS: FAIL — {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
